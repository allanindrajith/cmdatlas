#!/usr/bin/env python3
"""Validate commands.json and commands.csv integrity."""

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "data" / "commands.json"
CSV_PATH = ROOT / "data" / "commands.csv"

REQUIRED_FIELDS = [
    "id",
    "group",
    "groupLabel",
    "command",
    "summary",
    "example",
    "platform",
    "category",
    "install",
    "builtIn",
    "requiresAdmin",
    "riskLevel",
]
VALID_GROUPS = {"windows", "macos", "linux", "raspberry-pi", "docker-cross-platform"}
VALID_RISKS = {"safe", "caution", "deprecated"}


def main() -> int:
    errors = []

    if not JSON_PATH.exists():
        print(f"ERROR: Missing {JSON_PATH}")
        return 1
    if not CSV_PATH.exists():
        print(f"ERROR: Missing {CSV_PATH}")
        return 1

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        print("ERROR: commands.json must be a non-empty JSON array")
        return 1

    seen_ids = set()
    seen_commands = set()

    for idx, item in enumerate(data, start=1):
        for field in REQUIRED_FIELDS:
            if field not in item:
                errors.append(f"Row {idx}: missing field '{field}'")
            elif isinstance(item[field], str) and not item[field].strip():
                errors.append(f"Row {idx} ({item.get('id')}): empty string for '{field}'")

        cid = item.get("id")
        if cid in seen_ids:
            errors.append(f"Row {idx}: duplicate id '{cid}'")
        seen_ids.add(cid)

        cmd_key = (item.get("group"), item.get("command"))
        if cmd_key in seen_commands:
            errors.append(f"Row {idx}: duplicate command in group '{cmd_key}'")
        seen_commands.add(cmd_key)

        if item.get("group") not in VALID_GROUPS:
            errors.append(f"Row {idx} ({cid}): invalid group '{item.get('group')}'")
        if item.get("riskLevel") not in VALID_RISKS:
            errors.append(f"Row {idx} ({cid}): invalid riskLevel '{item.get('riskLevel')}'")
        if not isinstance(item.get("builtIn"), bool):
            errors.append(f"Row {idx} ({cid}): builtIn must be boolean")
        if not isinstance(item.get("requiresAdmin"), bool):
            errors.append(f"Row {idx} ({cid}): requiresAdmin must be boolean")

    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        csv_rows = list(csv.DictReader(f))

    if len(csv_rows) != len(data):
        errors.append(f"Row count mismatch: JSON has {len(data)}, CSV has {len(csv_rows)}")

    if errors:
        print("Validation FAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"Validation PASSED: {len(data)} commands verified across JSON and CSV.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
