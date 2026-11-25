#!/usr/bin/env python3
"""Run a synthetic placement-allocation demonstration with a fail-closed input gate.

This tool is not for real trainee or placement data. It accepts only the exact,
small synthetic schema below, rejects extra/free-text fields, and emits only
synthetic demo IDs and coded outputs. The gate is not a general PII detector.
"""
from __future__ import annotations

import argparse
import csv
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    import numpy as np
    from scipy.optimize import linear_sum_assignment
except ImportError:
    sys.exit("Missing dependency. Install requirements.txt to run the synthetic demo.")

YN = {"Yes", "No"}
PREF_COLS = ["pref1", "pref2", "pref3", "pref4"]
STUDENT_COLUMNS = ["demo_id", *PREF_COLS, "max_travel_minutes", "car_access", "required_specialty"]
PLACEMENT_COLUMNS = ["placement_id", "specialty", "capacity", "requires_car", "minimum_travel_minutes"]
PROVIDER_COLUMNS = ["placement_id", "demo_id", "placement_rank"]
RULE_COLUMNS = ["criterion", "weight"]
SPECIALTIES = {"CAMHS", "Adult", "Neuro", "LD"}
CRITERIA = {"student_preference", "placement_preference", "travel_fit"}
DEMO_ID = re.compile(r"D[0-9]{3,}\Z")
PLACEMENT_ID = re.compile(r"P[0-9]{3,}\Z")


class UnsafeInput(ValueError):
    """Input is outside the deliberately narrow synthetic demo format."""


def read_csv(path: Path, expected: list[str]) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            headers = reader.fieldnames or []
            if headers != expected:
                raise UnsafeInput(f"{path.name}: columns must exactly match the documented synthetic demo schema")
            rows = []
            for row_number, row in enumerate(reader, 2):
                if None in row or any(value is None for value in row.values()):
                    raise UnsafeInput(f"{path.name} row {row_number}: malformed row; input rejected")
                rows.append({key: (value or "").strip() for key, value in row.items()})
            return rows
    except OSError:
        raise UnsafeInput(f"{path.name}: cannot read synthetic demo input") from None
    except UnicodeError:
        raise UnsafeInput(f"{path.name}: invalid text encoding; input rejected") from None


def positive_int(value: str, field: str, errors: list[str], allow_zero: bool = False) -> int:
    try:
        number = int(value)
        if number < (0 if allow_zero else 1):
            raise ValueError
        return number
    except (ValueError, TypeError):
        errors.append(f"{field}: expected a {'non-negative' if allow_zero else 'positive'} integer")
        return 0


def validate(folder: Path):
    errors: list[str] = []
    students = read_csv(folder / "students.csv", STUDENT_COLUMNS)
    placements = read_csv(folder / "placements.csv", PLACEMENT_COLUMNS)
    provider = read_csv(folder / "placement_preferences.csv", PROVIDER_COLUMNS)
    rules = read_csv(folder / "allocation_rules.csv", RULE_COLUMNS)
    if not students or not placements:
        errors.append("student and placement demo files must not be empty")

    for row_no, student in enumerate(students, 2):
        tag = f"students.csv row {row_no}"
        if not DEMO_ID.fullmatch(student["demo_id"]):
            errors.append(f"{tag}: demo_id must use the synthetic D### format")
        if any(not PLACEMENT_ID.fullmatch(student[col]) for col in PREF_COLS):
            errors.append(f"{tag}: preferences must contain placement codes only")
        if len(set(student[col] for col in PREF_COLS)) != len(PREF_COLS):
            errors.append(f"{tag}: preferences must be distinct")
        positive_int(student["max_travel_minutes"], f"{tag} max_travel_minutes", errors)
        if student["car_access"] not in YN:
            errors.append(f"{tag}: car_access must be Yes or No")
        if student["required_specialty"] and student["required_specialty"] not in SPECIALTIES:
            errors.append(f"{tag}: required_specialty must be a synthetic category code or blank")

    student_ids = [row["demo_id"] for row in students]
    placement_ids = [row["placement_id"] for row in placements]
    if len(set(student_ids)) != len(student_ids):
        errors.append("students.csv: duplicate demo_id")
    if len(set(placement_ids)) != len(placement_ids):
        errors.append("placements.csv: duplicate placement_id")
    pids = set(placement_ids)
    specialties = {row["specialty"] for row in placements}
    capacities = {}
    for row_no, placement in enumerate(placements, 2):
        tag = f"placements.csv row {row_no}"
        if not PLACEMENT_ID.fullmatch(placement["placement_id"]):
            errors.append(f"{tag}: placement_id must use a synthetic P### code")
        if placement["specialty"] not in SPECIALTIES:
            errors.append(f"{tag}: specialty must be a synthetic category code")
        capacities[placement["placement_id"]] = positive_int(placement["capacity"], f"{tag} capacity", errors)
        positive_int(placement["minimum_travel_minutes"], f"{tag} minimum_travel_minutes", errors, allow_zero=True)
        if placement["requires_car"] not in YN:
            errors.append(f"{tag}: requires_car must be Yes or No")
    for row_no, student in enumerate(students, 2):
        if any(student[col] not in pids for col in PREF_COLS):
            errors.append(f"students.csv row {row_no}: unknown placement code in preferences")

    seen_pairs: set[tuple[str, str]] = set()
    ranks: dict[str, set[int]] = defaultdict(set)
    for row_no, rank_row in enumerate(provider, 2):
        tag = f"placement_preferences.csv row {row_no}"
        pid, did = rank_row["placement_id"], rank_row["demo_id"]
        if pid not in pids or did not in set(student_ids):
            errors.append(f"{tag}: unknown synthetic placement or demo ID")
        pair = (pid, did)
        if pair in seen_pairs:
            errors.append(f"{tag}: duplicate synthetic placement/demo pair")
        seen_pairs.add(pair)
        rank = positive_int(rank_row["placement_rank"], f"{tag} placement_rank", errors)
        if rank in ranks[pid]:
            errors.append(f"{tag}: duplicate rank for placement")
        ranks[pid].add(rank)

    weights: dict[str, float] = {}
    if {row["criterion"] for row in rules} != CRITERIA:
        errors.append("allocation_rules.csv: criteria must match the synthetic demo schema")
    for row_no, rule in enumerate(rules, 2):
        try:
            weight = float(rule["weight"])
            if not math.isfinite(weight) or not 0 <= weight <= 100:
                raise ValueError
            weights[rule["criterion"]] = weight
        except ValueError:
            errors.append(f"allocation_rules.csv row {row_no}: weight must be a finite number from 0 to 100")
    if weights and not math.isclose(sum(weights.values()), 100, abs_tol=1e-9):
        errors.append("allocation rule weights must total 100")
    if sum(capacities.values()) < len(students):
        errors.append("synthetic placement capacity is below the demo record count")
    return students, placements, provider, weights, errors


def solve(students, placements, provider, weights, banned=None):
    banned = banned or set()
    placement_map = {row["placement_id"]: row for row in placements}
    provider_rank = {(row["placement_id"], row["demo_id"]): int(row["placement_rank"]) for row in provider}
    max_rank = max(provider_rank.values(), default=1)
    slots = [row["placement_id"] for row in placements for _ in range(int(row["capacity"]))]
    n = len(students)
    slots += [f"UNALLOCATED_{i+1}" for i in range(max(0, n - len(slots)))]
    score = np.full((n, len(slots)), -1e9, dtype=float)
    detail = {}
    for i, student in enumerate(students):
        preferences = [student[col] for col in PREF_COLS]
        for j, pid in enumerate(slots):
            if pid.startswith("UNALLOCATED") or (student["demo_id"], pid) in banned:
                continue
            placement = placement_map[pid]
            if placement["requires_car"] == "Yes" and student["car_access"] != "Yes":
                continue
            if student["required_specialty"] and student["required_specialty"] != placement["specialty"]:
                continue
            travel = int(placement["minimum_travel_minutes"])
            limit = int(student["max_travel_minutes"])
            if travel > limit:
                continue
            rank = preferences.index(pid) + 1 if pid in preferences else 5
            student_score = {1: 100, 2: 75, 3: 50, 4: 25}.get(rank, 0)
            provider_position = provider_rank.get((pid, student["demo_id"]))
            provider_score = 0 if provider_position is None else max(0, 100 - (provider_position - 1) * (100 / max(1, max_rank)))
            travel_score = max(0, 100 * (limit - travel) / max(1, limit))
            total = (weights["student_preference"] * student_score + weights["placement_preference"] * provider_score + weights["travel_fit"] * travel_score) / 100
            score[i, j] = total
            detail[(i, j)] = (rank, student_score, provider_score, travel_score, total)
    rows, cols = linear_sum_assignment(-score)
    if any(score[i, j] < -1e8 for i, j in zip(rows, cols)):
        return None
    result = []
    for i, j in zip(rows, cols):
        pid = slots[j]
        rank, student_score, provider_score, travel_score, total = detail[(i, j)]
        result.append({"demo_id": students[i]["demo_id"], "placement_id": pid, "preference_achieved": rank,
                       "student_preference_score": round(student_score, 2), "placement_preference_score": round(provider_score, 2),
                       "travel_fit_score": round(travel_score, 2), "total_score": round(total, 2)})
    return sorted(result, key=lambda row: row["demo_id"])


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Synthetic placement-allocation demonstration only; real/personal data is not accepted.")
    parser.add_argument("--input-dir", default=".")
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--options", type=int, default=3)
    args = parser.parse_args()
    folder, output = Path(args.input_dir), Path(args.output_dir)
    try:
        students, placements, provider, weights, errors = validate(folder)
    except UnsafeInput as exc:
        errors = [str(exc)]
        students = placements = provider = []
        weights = {}
    output.mkdir(parents=True, exist_ok=True)
    report = [{"severity": "ERROR", "message": message} for message in errors]
    if not report:
        report = [{"severity": "INFO", "message": "Synthetic demo schema passed; this is not an approval for real use."}]
    write_csv(output / "validation_report.csv", report)
    if errors:
        print(f"Input rejected; {len(errors)} schema/format issue(s). No allocation was run. See validation_report.csv.", file=sys.stderr)
        return 2
    options, banned = [], set()
    for option_no in range(1, max(1, args.options) + 1):
        solved = solve(students, placements, provider, weights, banned)
        if not solved:
            break
        options.extend({"option": option_no, **row} for row in solved)
        lowest = min(solved, key=lambda row: row["total_score"])
        banned.add((lowest["demo_id"], lowest["placement_id"]))
    write_csv(output / "allocation_options.csv", options)
    best = [{key: value for key, value in row.items() if key != "option"} for row in options if row["option"] == 1]
    write_csv(output / "allocation_results.csv", best)
    summary = []
    if best:
        summary = [{"metric": "demo_records_allocated", "value": len(best)},
                   {"metric": "first_choice_count", "value": sum(row["preference_achieved"] == 1 for row in best)},
                   {"metric": "top_two_count", "value": sum(row["preference_achieved"] <= 2 for row in best)},
                   {"metric": "mean_score", "value": round(sum(row["total_score"] for row in best) / len(best), 2)}]
    write_csv(output / "allocation_summary.csv", summary)
    print(f"Created {len({row['option'] for row in options})} synthetic demo option(s) in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
