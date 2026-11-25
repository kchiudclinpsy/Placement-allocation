#!/usr/bin/env python3
"""Validate the repository's synthetic demonstration data only.

This report is not a readiness assessment, approval, or validation for any real
placement process. Only run this script against the synthetic example files.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
errors: list[str] = []
warnings: list[str] = []


def load(name: str, required: tuple[str, ...]) -> list[dict[str, str]]:
    path = ROOT / name
    try:
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            missing = [column for column in required if column not in (reader.fieldnames or [])]
            if missing:
                errors.append(f"{name}: missing columns {missing}")
            return list(reader)
    except OSError as exc:
        errors.append(f"{name}: could not read file ({exc})")
        return []


def unique(rows: list[dict[str, str]], key: str, name: str) -> None:
    values = [row[key] for row in rows if row.get(key)]
    if len(values) != len(set(values)):
        errors.append(f"{name}: duplicate {key}")


trainees = load("trainees.csv", ("trainee_id", "cohort_id", "training_year", "next_placement_number", "base_code", "driving_access", "allocation_status"))
offers = load("placement_offers.csv", ("offer_id", "placement_id", "rotation_id", "capacity", "approved", "quality_status", "supervisor_approved", "weekly_supervision_minutes", "weekly_contact_minutes", "cover_arrangement_confirmed"))
capabilities = load("placement_capabilities.csv", ("placement_id", "capability_type", "capability_code", "opportunity_strength"))
history = load("placement_history.csv", ("trainee_id", "placement_number", "placement_id", "rotation_id", "outcome", "attendance_days", "competency_evidence_signed_off"))
competencies = load("competency_status.csv", ("trainee_id", "competency_code", "status", "evidence_date", "source_placement_number"))
preferences = load("specialist_preferences.csv", ("trainee_id", "rotation_id", "placement_id", "rank", "advisor_reviewed"))
flags = load("review_flags.csv", ("trainee_id", "flag_code", "valid_from", "valid_to", "review_status"))
policy = load("allocation_policy.csv", ("policy_version", "rule_id", "stage", "rule_type", "criterion", "weight", "enabled"))

unique(trainees, "trainee_id", "trainees.csv")
unique(offers, "offer_id", "placement_offers.csv")
trainee_ids = {row.get("trainee_id", "") for row in trainees}
placement_ids = {row.get("placement_id", "") for row in offers}

for row in trainees:
    if row.get("training_year") not in {"1", "2", "3"}:
        errors.append(f"{row.get('trainee_id', 'unknown')}: training_year must be 1..3")
    if row.get("next_placement_number") not in {"1", "2", "3", "4", "5", "6"}:
        errors.append(f"{row.get('trainee_id', 'unknown')}: next_placement_number must be 1..6")
    if row.get("driving_access") not in {"Yes", "No", "Adjustment"}:
        errors.append(f"{row.get('trainee_id', 'unknown')}: invalid driving_access")

for row in offers:
    tag = row.get("offer_id", "unknown offer")
    for key in ("approved", "supervisor_approved", "cover_arrangement_confirmed"):
        if row.get(key) not in {"Yes", "No"}:
            errors.append(f"{tag}: {key} must be Yes or No")
    try:
        if int(row.get("capacity", "")) < 1:
            raise ValueError
        supervision = int(row.get("weekly_supervision_minutes", ""))
        int(row.get("weekly_contact_minutes", ""))
        if supervision < 60:
            warnings.append(f"{tag}: weekly supervision is below 60 minutes (example value only; not an official standard)")
    except ValueError:
        errors.append(f"{tag}: invalid numeric capacity/supervision/contact")
    if row.get("quality_status") == "Suspended":
        errors.append(f"{tag}: suspended example placement cannot be offered")
    if row.get("approved") != "Yes" or row.get("supervisor_approved") != "Yes":
        errors.append(f"{tag}: example approval incomplete")
    if row.get("cover_arrangement_confirmed") != "Yes":
        errors.append(f"{tag}: example supervision cover not confirmed")

for name, rows in (("history", history), ("competency", competencies), ("specialist_preferences", preferences), ("review_flags", flags)):
    for row in rows:
        if row.get("trainee_id") and row["trainee_id"] not in trainee_ids:
            errors.append(f"{name}: unknown trainee {row['trainee_id']}")
for row in preferences:
    if row.get("placement_id") not in placement_ids:
        errors.append(f"specialist_preferences: unknown placement {row.get('placement_id')}")
    if row.get("advisor_reviewed") != "Yes":
        warnings.append(f"specialist preference not advisor-reviewed for {row.get('trainee_id', 'unknown trainee')}")

try:
    soft_weights = sum(float(row.get("weight") or 0) for row in policy if row.get("rule_type") == "Soft" and row.get("enabled") == "Yes")
    if abs(soft_weights - 100) > 0.001:
        errors.append(f"enabled example soft weights total {soft_weights}, not 100")
except ValueError:
    errors.append("allocation_policy.csv: invalid numeric soft weight")

report = [["severity", "message"]]
report.extend([["ERROR", message] for message in errors])
report.extend([["WARNING", message] for message in warnings])
if not errors and not warnings:
    report.append(["INFO", "Synthetic demo data validation passed; this is not approval for real use"])
with (ROOT / "readiness_report.csv").open("w", newline="", encoding="utf-8") as stream:
    csv.writer(stream).writerows(report)
print(f"Demo-data errors: {len(errors)}; warnings: {len(warnings)}")
sys.exit(2 if errors else 0)
