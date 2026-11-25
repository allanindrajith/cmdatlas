#!/usr/bin/env python3
"""Convert the 'All Commands' sheet of CmdAtlas_expanded_commands_audited.xlsx
into per-platform JSON files for the Community collection tier.

Uses only the Python standard library so it runs without third-party packages.
Ignores the 'Excluded (not commands)' sheet completely.
"""

from collections import Counter
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
import zipfile

NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL_NS = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}

PLATFORM_MAP = {
    "Windows": ("windows", "Windows"),
    "Windows (DOS legacy)": ("windows", "Windows"),
    "macOS": ("macos", "macOS"),
    "Linux": ("linux", "Linux"),
    "Raspberry Pi OS": ("raspberry-pi", "Raspberry Pi"),
    "Docker": ("docker", "Docker"),
    "Cross-platform (common)": ("cross-platform", "Cross-Platform"),
}

VALID_PUBLIC_LABELS = {
    "Tested (Linux/Docker sandbox)",
    "Source-verified (official docs)",
    "Community-sourced (not tested)",
    "Unverified (Reddit post)",
}

PLATFORM_ORDER = [
    "windows",
    "macos",
    "linux",
    "raspberry-pi",
    "docker",
    "cross-platform",
]


def col_idx(ref: str) -> int:
    col = "".join(ch for ch in ref if ch.isalpha())
    n = 0
    for ch in col:
        n = n * 26 + (ord(ch.upper()) - ord("A") + 1)
    return n - 1


def get_cell_val(cell: ET.Element, sst: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        is_el = cell.find("s:is", NS)
        if is_el is not None:
            return "".join(el.text or "" for el in is_el.findall(".//s:t", NS))
        return ""
    v_el = cell.find("s:v", NS)
    if v_el is None:
        return ""
    if cell_type == "s":
        return sst[int(v_el.text)]
    return v_el.text or ""


def find_sheet_path(zf: zipfile.ZipFile, sheet_name: str) -> str:
    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_map = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels.findall("r:Relationship", REL_NS)
    }
    for sheet in wb.findall(".//s:sheet", NS):
        if sheet.attrib.get("name") == sheet_name:
            rid = sheet.attrib.get(
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
            )
            target = rel_map[rid].lstrip("/")
            return target if target.startswith("xl/") else f"xl/{target}"
    raise ValueError(f"Sheet '{sheet_name}' not found in workbook")


def parse_row(row_el: ET.Element, sst: list[str], width: int | None = None) -> list[str]:
    vals = {
        col_idx(c.attrib["r"]): get_cell_val(c, sst)
        for c in row_el.findall("s:c", NS)
    }
    w = width if width is not None else (max(vals) + 1 if vals else 0)
    return [vals.get(i, "") for i in range(w)]


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    workspace_root = repo_root.parent
    xlsx_path = workspace_root / "CmdAtlas_expanded_commands_audited.xlsx"

    if not xlsx_path.exists():
        print(f"ERROR: Workbook not found at {xlsx_path}", file=sys.stderr)
        return 1

    with zipfile.ZipFile(xlsx_path) as zf:
        sst: list[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            sst_root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in sst_root.findall("s:si", NS):
                sst.append("".join(t.text or "" for t in si.findall(".//s:t", NS)))

        sheet_path = find_sheet_path(zf, "All Commands")
        root = ET.fromstring(zf.read(sheet_path))
        rows = root.findall(".//s:sheetData/s:row", NS)

    headers = parse_row(rows[0], sst)
    h = {name: i for i, name in enumerate(headers)}

    grouped: dict[str, list[dict]] = {slug: [] for slug in PLATFORM_ORDER}
    label_totals: Counter[str] = Counter()
    per_platform_labels: dict[str, Counter[str]] = {
        slug: Counter() for slug in PLATFORM_ORDER
    }

    for r_idx, row_el in enumerate(rows[1:], start=2):
        vals = parse_row(row_el, sst, len(headers))
        platform_raw = vals[h["Platform"]].strip()
        if platform_raw not in PLATFORM_MAP:
            raise ValueError(f"Row {r_idx}: unexpected platform '{platform_raw}'")

        group_slug, group_label = PLATFORM_MAP[platform_raw]
        public_label = vals[h["Public label"]].strip()
        if public_label not in VALID_PUBLIC_LABELS:
            raise ValueError(f"Row {r_idx}: unexpected public label '{public_label}'")

        risk_flag = vals[h["Risk flag"]].strip()
        risk_level = "caution" if "CAUTION" in risk_flag.upper() else "safe"
        requires_admin = "needs sudo/admin" in risk_flag.lower()

        entry = {
            "id": vals[h["ID"]].strip(),
            "group": group_slug,
            "groupLabel": group_label,
            "command": vals[h["Command"]].strip(),
            "summary": vals[h["What it does"]].strip(),
            "example": "",
            "platform": platform_raw,
            "category": vals[h["Tool"]].strip(),
            "install": "",
            "builtIn": False,
            "requiresAdmin": requires_admin,
            "riskLevel": risk_level,
            "riskFlag": risk_flag,
            "publicLabel": public_label,
            "sourceUrl": vals[h["Source URL"]].strip(),
            "license": vals[h["License / attribution"]].strip(),
            "readyToRun": vals[h["Ready to run as-is?"]].strip(),
        }

        grouped[group_slug].append(entry)
        label_totals[public_label] += 1
        per_platform_labels[group_slug][public_label] += 1

    out_dirs = [
        repo_root / "data" / "community",
        workspace_root / "website" / "data" / "community",
    ]

    manifest = {
        "total": sum(len(v) for v in grouped.values()),
        "labels": dict(label_totals),
        "platforms": [],
    }

    for slug in PLATFORM_ORDER:
        items = grouped[slug]
        group_label = items[0]["groupLabel"] if items else slug
        manifest["platforms"].append(
            {
                "slug": slug,
                "label": group_label,
                "file": f"{slug}.json",
                "count": len(items),
                "labels": dict(per_platform_labels[slug]),
            }
        )

    for out_dir in out_dirs:
        out_dir.mkdir(parents=True, exist_ok=True)
        for slug in PLATFORM_ORDER:
            out_file = out_dir / f"{slug}.json"
            # Compact JSON keeps large platform files (e.g. cross-platform) fast to download
            out_file.write_text(
                json.dumps(grouped[slug], ensure_ascii=False, separators=(",", ":")),
                encoding="utf-8",
            )
        (out_dir / "index.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(f"Exported {manifest['total']} community commands to {len(PLATFORM_ORDER)} platform files.")
    for p in manifest["platforms"]:
        size_kb = (out_dirs[0] / p["file"]).stat().st_size / 1024
        print(f"  {p['slug']:15s}: {p['count']:6d} rows ({size_kb:,.1f} KB)")
    print("Public labels:")
    for lbl, cnt in label_totals.most_common():
        print(f"  {lbl}: {cnt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
