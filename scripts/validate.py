#!/usr/bin/env python3
"""Validate Verified core (commands.json / commands.csv), Community collection, and AI CLI JSON files."""

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "data" / "commands.json"
CSV_PATH = ROOT / "data" / "commands.csv"
COMMUNITY_DIR = ROOT / "data" / "community"
AI_DIR = ROOT / "data" / "ai"

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

COMMUNITY_REQUIRED_FIELDS = REQUIRED_FIELDS + [
    "riskFlag",
    "publicLabel",
    "sourceUrl",
    "license",
    "readyToRun",
]

# Fields that may legitimately be empty strings on community rows (not present in source xlsx)
COMMUNITY_ALLOW_EMPTY = {"example", "install", "riskFlag"}

VALID_GROUPS = {"windows", "macos", "linux", "raspberry-pi", "docker-cross-platform"}
COMMUNITY_GROUPS = [
    "windows",
    "macos",
    "linux",
    "raspberry-pi",
    "docker",
    "cross-platform",
]
VALID_RISKS = {"safe", "caution", "deprecated"}
VALID_PUBLIC_LABELS = {
    "Tested (Linux/Docker sandbox)",
    "Source-verified (official docs)",
    "Community-sourced (not tested)",
    "Unverified (Reddit post)",
}
AI_REQUIRED_FIELDS = [
    "id",
    "group",
    "groupLabel",
    "tool",
    "toolSlug",
    "toolCommand",
    "type",
    "command",
    "summary",
    "descriptionStatus",
    "platform",
    "category",
    "readyToRun",
    "riskLevel",
    "riskFlag",
    "publicLabel",
    "sourceUrl",
    "version",
    "license",
    "dateChecked",
]
AI_ALLOW_EMPTY = {"summary", "riskFlag", "version", "license"}
AI_VALID_PUBLIC_LABELS = {
    "Tested (ran --help, Linux sandbox)",
    "Tested (installed CLI --help, Linux sandbox)",
    "Source-verified (official docs)",
    "Source-verified (official source code)",
    "Community-sourced (not tested)",
}
AI_VALID_TYPES = {
    "Shell command",
    "Flag / option",
    "In-app slash command",
    "Install",
}


def validate_core(errors: list[str], seen_ids: set[str]) -> int:
    if not JSON_PATH.exists():
        errors.append(f"Missing {JSON_PATH}")
        return 0
    if not CSV_PATH.exists():
        errors.append(f"Missing {CSV_PATH}")
        return 0

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        errors.append("commands.json must be a non-empty JSON array")
        return 0

    seen_commands = set()

    for idx, item in enumerate(data, start=1):
        for field in REQUIRED_FIELDS:
            if field not in item:
                errors.append(f"Core row {idx}: missing field '{field}'")
            elif isinstance(item[field], str) and not item[field].strip():
                errors.append(f"Core row {idx} ({item.get('id')}): empty string for '{field}'")

        cid = item.get("id")
        if cid in seen_ids:
            errors.append(f"Core row {idx}: duplicate id '{cid}'")
        seen_ids.add(cid)

        cmd_key = (item.get("group"), item.get("command"))
        if cmd_key in seen_commands:
            errors.append(f"Core row {idx}: duplicate command in group '{cmd_key}'")
        seen_commands.add(cmd_key)

        if item.get("group") not in VALID_GROUPS:
            errors.append(f"Core row {idx} ({cid}): invalid group '{item.get('group')}'")
        if item.get("riskLevel") not in VALID_RISKS:
            errors.append(f"Core row {idx} ({cid}): invalid riskLevel '{item.get('riskLevel')}'")
        if not isinstance(item.get("builtIn"), bool):
            errors.append(f"Core row {idx} ({cid}): builtIn must be boolean")
        if not isinstance(item.get("requiresAdmin"), bool):
            errors.append(f"Core row {idx} ({cid}): requiresAdmin must be boolean")

    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        csv_rows = list(csv.DictReader(f))

    if len(csv_rows) != len(data):
        errors.append(f"Core row count mismatch: JSON has {len(data)}, CSV has {len(csv_rows)}")

    return len(data)


def validate_community(errors: list[str], seen_ids: set[str]) -> tuple[dict[str, int], Counter]:
    platform_counts: dict[str, int] = {}
    label_counts: Counter = Counter()

    if not COMMUNITY_DIR.exists():
        errors.append(f"Missing community data directory {COMMUNITY_DIR}")
        return platform_counts, label_counts

    for slug in COMMUNITY_GROUPS:
        path = COMMUNITY_DIR / f"{slug}.json"
        if not path.exists():
            errors.append(f"Missing community platform file {path}")
            continue

        rows = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(rows, list) or not rows:
            errors.append(f"{path.name}: must be a non-empty JSON array")
            continue

        platform_counts[slug] = len(rows)

        for idx, item in enumerate(rows, start=1):
            cid = item.get("id")
            for field in COMMUNITY_REQUIRED_FIELDS:
                if field not in item:
                    errors.append(f"{path.name} row {idx} ({cid}): missing field '{field}'")
                elif (
                    field not in COMMUNITY_ALLOW_EMPTY
                    and isinstance(item[field], str)
                    and not item[field].strip()
                ):
                    errors.append(f"{path.name} row {idx} ({cid}): empty string for '{field}'")

            if cid in seen_ids:
                errors.append(f"{path.name} row {idx}: duplicate id '{cid}'")
            seen_ids.add(cid)

            if item.get("group") != slug:
                errors.append(
                    f"{path.name} row {idx} ({cid}): group '{item.get('group')}' does not match file '{slug}'"
                )
            if item.get("riskLevel") not in VALID_RISKS:
                errors.append(f"{path.name} row {idx} ({cid}): invalid riskLevel '{item.get('riskLevel')}'")
            if not isinstance(item.get("builtIn"), bool):
                errors.append(f"{path.name} row {idx} ({cid}): builtIn must be boolean")
            if not isinstance(item.get("requiresAdmin"), bool):
                errors.append(f"{path.name} row {idx} ({cid}): requiresAdmin must be boolean")

            pub_label = item.get("publicLabel")
            if pub_label not in VALID_PUBLIC_LABELS:
                errors.append(f"{path.name} row {idx} ({cid}): invalid publicLabel '{pub_label}'")
            else:
                label_counts[pub_label] += 1

            src_url = item.get("sourceUrl", "")
            if not (src_url.startswith("http://") or src_url.startswith("https://")):
                errors.append(f"{path.name} row {idx} ({cid}): invalid sourceUrl '{src_url}'")

            if len(errors) > 50:
                errors.append("Too many errors; aborting remaining checks.")
                return platform_counts, label_counts

    index_path = COMMUNITY_DIR / "index.json"
    if not index_path.exists():
        errors.append(f"Missing community manifest {index_path}")
    else:
        manifest = json.loads(index_path.read_text(encoding="utf-8"))
        total_actual = sum(platform_counts.values())
        if manifest.get("total") != total_actual:
            errors.append(
                f"index.json total ({manifest.get('total')}) != actual sum ({total_actual})"
            )

    return platform_counts, label_counts


def validate_ai(errors: list[str], seen_ids: set[str]) -> tuple[dict[str, int], Counter]:
    tool_counts: dict[str, int] = {}
    label_counts: Counter = Counter()

    if not AI_DIR.exists():
        errors.append(f"Missing AI CLI data directory {AI_DIR}")
        return tool_counts, label_counts

    index_path = AI_DIR / "index.json"
    if not index_path.exists():
        errors.append(f"Missing AI CLI manifest {index_path}")
        return tool_counts, label_counts

    manifest = json.loads(index_path.read_text(encoding="utf-8"))
    tools = manifest.get("tools", [])
    if not isinstance(tools, list) or not tools:
        errors.append("data/ai/index.json: 'tools' must be a non-empty array")
        return tool_counts, label_counts

    for tool_meta in tools:
        slug = tool_meta.get("slug")
        fname = tool_meta.get("file")
        path = AI_DIR / fname if fname else AI_DIR / f"{slug}.json"
        if not path.exists():
            errors.append(f"Missing AI CLI tool file {path}")
            continue

        rows = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(rows, list) or not rows:
            errors.append(f"data/ai/{path.name}: must be a non-empty JSON array")
            continue

        tool_counts[slug] = len(rows)
        if tool_meta.get("count") != len(rows):
            errors.append(
                f"data/ai/index.json count for '{slug}' ({tool_meta.get('count')}) != file rows ({len(rows)})"
            )

        for idx, item in enumerate(rows, start=1):
            cid = item.get("id")
            for field in AI_REQUIRED_FIELDS:
                if field not in item:
                    errors.append(f"ai/{path.name} row {idx} ({cid}): missing field '{field}'")
                elif (
                    field not in AI_ALLOW_EMPTY
                    and isinstance(item[field], str)
                    and not item[field].strip()
                ):
                    errors.append(f"ai/{path.name} row {idx} ({cid}): empty string for '{field}'")

            if cid in seen_ids:
                errors.append(f"ai/{path.name} row {idx}: duplicate id '{cid}'")
            seen_ids.add(cid)

            if item.get("toolSlug") != slug:
                errors.append(
                    f"ai/{path.name} row {idx} ({cid}): toolSlug '{item.get('toolSlug')}' != '{slug}'"
                )
            if item.get("riskLevel") not in VALID_RISKS:
                errors.append(f"ai/{path.name} row {idx} ({cid}): invalid riskLevel '{item.get('riskLevel')}'")
            if item.get("type") not in AI_VALID_TYPES:
                errors.append(f"ai/{path.name} row {idx} ({cid}): invalid type '{item.get('type')}'")
            if item.get("descriptionStatus") == "ok" and not item.get("summary", "").strip():
                errors.append(f"ai/{path.name} row {idx} ({cid}): empty summary with descriptionStatus='ok'")

            pub_label = item.get("publicLabel")
            if pub_label not in AI_VALID_PUBLIC_LABELS:
                errors.append(f"ai/{path.name} row {idx} ({cid}): invalid publicLabel '{pub_label}'")
            else:
                label_counts[pub_label] += 1

            src_url = item.get("sourceUrl", "")
            if not (src_url.startswith("http://") or src_url.startswith("https://")):
                errors.append(f"ai/{path.name} row {idx} ({cid}): invalid sourceUrl '{src_url}'")

            if len(errors) > 50:
                errors.append("Too many errors; aborting remaining AI CLI checks.")
                return tool_counts, label_counts

    total_actual = sum(tool_counts.values())
    if manifest.get("total") != total_actual:
        errors.append(f"data/ai/index.json total ({manifest.get('total')}) != actual sum ({total_actual})")

    all_path = AI_DIR / "all.json"
    if not all_path.exists():
        errors.append(f"Missing combined AI CLI dataset {all_path}")
    else:
        all_rows = json.loads(all_path.read_text(encoding="utf-8"))
        if len(all_rows) != total_actual:
            errors.append(f"data/ai/all.json row count ({len(all_rows)}) != per-tool sum ({total_actual})")

    return tool_counts, label_counts


def main() -> int:
    errors: list[str] = []
    seen_ids: set[str] = set()

    core_count = validate_core(errors, seen_ids)
    platform_counts, label_counts = validate_community(errors, seen_ids)
    ai_tool_counts, ai_label_counts = validate_ai(errors, seen_ids)

    if errors:
        print("Validation FAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1

    comm_total = sum(platform_counts.values())
    ai_total = sum(ai_tool_counts.values())
    print("Validation PASSED:")
    print(f"  Verified core:        {core_count} commands (JSON + CSV)")
    print(f"  Community collection: {comm_total} commands across {len(platform_counts)} platform files")
    for slug in COMMUNITY_GROUPS:
        print(f"    - {slug:15s}: {platform_counts.get(slug, 0)}")
    print("  Community public labels:")
    for lbl in [
        "Tested (Linux/Docker sandbox)",
        "Source-verified (official docs)",
        "Community-sourced (not tested)",
        "Unverified (Reddit post)",
    ]:
        print(f"    - {lbl}: {label_counts.get(lbl, 0)}")
    print(f"  AI CLI collection:    {ai_total} commands across {len(ai_tool_counts)} tools")
    print("  AI CLI public labels:")
    for lbl, count in ai_label_counts.most_common():
        print(f"    - {lbl}: {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
