#!/usr/bin/env python3
import json
import time
from pathlib import Path

from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.metadata import schema_classes as sc


ACTOR = "urn:li:corpuser:agenthack"
PLATFORM = "urn:li:dataPlatform:postgres"
PII_TAG = "urn:li:tag:PII"
SECURITY_TAG = "urn:li:tag:security_review"


def dataset_urn(name: str) -> str:
    return f"urn:li:dataset:(urn:li:dataPlatform:postgres,{name},PROD)"


def mcp(entity_urn: str, aspect) -> dict:
    return MetadataChangeProposalWrapper(entityUrn=entity_urn, aspect=aspect).to_obj()


def schema(name: str, fields: list[tuple[str, str, str | None]]) -> sc.SchemaMetadataClass:
    return sc.SchemaMetadataClass(
        schemaName=name,
        platform=PLATFORM,
        version=0,
        hash="",
        platformSchema=sc.OtherSchemaClass(rawSchema="clean-room hackathon schema"),
        fields=[
            sc.SchemaFieldClass(
                fieldPath=field_name,
                type=sc.SchemaFieldDataTypeClass(type=sc.StringTypeClass()),
                nativeDataType=native_type,
                nullable=True,
                description=description,
                globalTags=(
                    sc.GlobalTagsClass(tags=[sc.TagAssociationClass(tag=PII_TAG)])
                    if "email" in field_name or "ssn" in field_name
                    else None
                ),
            )
            for field_name, native_type, description in fields
        ],
    )


def ownership(owner: str | None) -> sc.OwnershipClass | None:
    if not owner:
        return None
    return sc.OwnershipClass(
        owners=[
            sc.OwnerClass(
                owner=f"urn:li:corpuser:{owner}",
                type=sc.OwnershipTypeClass.DATAOWNER,
            )
        ]
    )


def browse_path(domain: str, name: str) -> sc.BrowsePathsV2Class:
    return sc.BrowsePathsV2Class(
        path=[
            sc.BrowsePathEntryClass(id="prod"),
            sc.BrowsePathEntryClass(id=domain),
            sc.BrowsePathEntryClass(id=name),
        ]
    )


def dataset_records(name: str, description: str, owner: str | None, fields, upstreams=None):
    urn = dataset_urn(name)
    records = [
        mcp(urn, sc.StatusClass(removed=False)),
        mcp(
            urn,
            sc.DatasetPropertiesClass(
                name=name,
                description=description,
                customProperties={
                    "freshness_slo_hours": "24",
                    "last_observed_hours_ago": "96" if owner is None else "6",
                    "control_plane": "clean-room-agenthack",
                },
            ),
        ),
        mcp(urn, schema(name, fields)),
        mcp(urn, browse_path("security-governance", name)),
        mcp(urn, sc.GlobalTagsClass(tags=[sc.TagAssociationClass(tag=SECURITY_TAG)])),
    ]
    own = ownership(owner)
    if own:
        records.append(mcp(urn, own))
    if upstreams:
        records.append(
            mcp(
                urn,
                sc.UpstreamLineageClass(
                    upstreams=[
                        sc.UpstreamClass(dataset=dataset_urn(up), type=sc.DatasetLineageTypeClass.TRANSFORMED)
                        for up in upstreams
                    ]
                ),
            )
        )
    return records


def main() -> None:
    out = Path("metadata/cleanroom_security_catalog.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    records = []
    records.extend(
        dataset_records(
            "warehouse.raw_customer_profiles",
            "Raw customer profile table. Contains email and SSN-like sample fields; owner intentionally missing.",
            None,
            [
                ("customer_id", "varchar", "Stable customer identifier"),
                ("email", "varchar", "PII-tagged email address"),
                ("ssn_last4", "varchar", "PII-tagged synthetic SSN suffix"),
            ],
        )
    )
    records.extend(
        dataset_records(
            "warehouse.raw_orders",
            "Raw orders table. Owned by analytics-eng and refreshed within SLO.",
            "analytics_eng",
            [
                ("order_id", "varchar", "Order identifier"),
                ("customer_id", "varchar", "Foreign key to raw_customer_profiles"),
                ("total_amount", "decimal", "Order total"),
            ],
        )
    )
    records.extend(
        dataset_records(
            "warehouse.customer_risk_features",
            "Feature table consumed by downstream risk scoring. Inherits PII from raw profiles.",
            "ml_platform",
            [
                ("customer_id", "varchar", "Customer identifier"),
                ("email_domain", "varchar", "Derived from email; still privacy-sensitive"),
                ("risk_score", "double", "Model feature"),
            ],
            upstreams=["warehouse.raw_customer_profiles", "warehouse.raw_orders"],
        )
    )
    records.extend(
        dataset_records(
            "warehouse.public_revenue_summary",
            "Public dashboard rollup without direct PII fields.",
            "bi_team",
            [
                ("week", "date", "Reporting week"),
                ("revenue", "decimal", "Weekly revenue"),
            ],
            upstreams=["warehouse.raw_orders"],
        )
    )

    # Add a generated timestamp as metadata only, not as security evidence.
    for record in records:
        record.setdefault("headers", {})["generated_at_epoch_ms"] = str(int(time.time() * 1000))

    out.write_text(json.dumps(records, indent=2) + "\n")
    print(f"Wrote {len(records)} MCP records to {out}")


if __name__ == "__main__":
    main()
