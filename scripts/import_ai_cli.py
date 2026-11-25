#!/usr/bin/env python3
"""Convert 'All Commands' and 'Tools Coverage' from CmdAtlas_AI_CLI_commands_audited.xlsx
into CmdAtlas AI CLI JSON datasets, an internal rewording queue, and static HTML pages.

Uses only the Python standard library so it runs without third-party packages.
Reads ONLY 'All Commands' as command data (6,005 rows in -> 6,005 rows out).
"""

from collections import Counter
import html
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL_NS = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}

TOOL_SLUGS = {
    "Aider": "aider",
    "Antigravity CLI": "antigravity-cli",
    "Claude Code": "claude-code",
    "Codex CLI": "codex-cli",
    "Cursor CLI": "cursor-cli",
    "DeepSeek Harness": "deepseek-harness",
    "Gemini CLI": "gemini-cli",
    "GitHub Copilot CLI": "github-copilot-cli",
    "Hermes Agent (Nous Research)": "hermes-agent",
    "Hugging Face CLI (hf)": "huggingface-cli",
    "Kimi Code CLI": "kimi-code-cli",
    "Mistral Vibe": "mistral-vibe",
    "Ollama": "ollama",
    "OpenClaw": "openclaw",
    "OpenCode": "opencode",
    "Osaurus": "osaurus",
    "Qwen Code": "qwen-code",
    "Windsurf": "windsurf",
    "ZCode": "zcode",
    "llama.cpp": "llama-cpp",
    "llm (Simon Willison)": "llm",
}

REQUIRED_TOOL_NOTES = {
    "Windsurf": "IDE-first, no official CLI reference",
    "Gemini CLI": "Legacy: being replaced by Antigravity CLI (agy)",
}

VALID_PUBLIC_LABELS = {
    "Tested (ran --help, Linux sandbox)",
    "Tested (installed CLI --help, Linux sandbox)",
    "Source-verified (official docs)",
    "Source-verified (official source code)",
    "Community-sourced (not tested)",
}

VALID_TYPES = {
    "Shell command",
    "Flag / option",
    "In-app slash command",
    "Install",
}

SITE_WIDE_NOTICE = (
    "Most AI CLI rows come from official docs or source and have not been run. "
    "Tools change monthly; check the date on each page."
)


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


def load_sheet_rows(zf: zipfile.ZipFile, sst: list[str], sheet_name: str) -> list[list[str]]:
    sheet_path = find_sheet_path(zf, sheet_name)
    root = ET.fromstring(zf.read(sheet_path))
    raw_rows = root.findall(".//s:sheetData/s:row", NS)
    if not raw_rows:
        return []
    headers = parse_row(raw_rows[0], sst)
    width = len(headers)
    out = [headers]
    for row_el in raw_rows[1:]:
        vals = parse_row(row_el, sst, width)
        if any(v != "" for v in vals):
            out.append(vals)
    return out


def esc(val: str) -> str:
    return html.escape(val, quote=True)


def render_page_html(
    *,
    is_all: bool,
    tool_meta: dict | None,
    all_tools: list[dict],
    total_rows: int,
    date_checked: str,
) -> str:
    if is_all:
        page_title = "AI CLI Commands — All 21 Tools — CmdAtlas"
        meta_desc = (
            f"Searchable reference of {total_rows:,} AI CLI commands, flags, install snippets, "
            f"and in-app slash commands across {len(all_tools)} AI developer tools."
        )
        canonical = "https://itsallan.me/cmdatlas/ai/"
        body_attrs = 'data-ai-page="all" data-ai-tool="all"'
        hero_h1 = "AI CLI commands, clearly labeled."
        hero_lead = (
            f"{total_rows:,} commands, flags, install snippets, and in-app slash commands "
            f"across {len(all_tools)} AI CLI tools."
        )
        tool_header_html = ""
    else:
        assert tool_meta is not None
        tname = tool_meta["name"]
        slug = tool_meta["slug"]
        tcmd = tool_meta["command"]
        trows = tool_meta["count"]
        tmethod = tool_meta["method"]
        tversion = tool_meta["version"]
        tnote = tool_meta["note"]
        tdate = tool_meta["dateChecked"] or date_checked

        page_title = f"{tname} ({tcmd}) CLI Commands — CmdAtlas"
        meta_desc = (
            f"{trows:,} {tname} ({tcmd}) commands, flags, and slash commands. "
            f"Checked {tdate}. {tmethod}"
        )
        canonical = f"https://itsallan.me/cmdatlas/ai/{slug}.html"
        body_attrs = f'data-ai-page="tool" data-ai-tool="{esc(slug)}"'
        hero_h1 = f"{tname}, docs checked {tdate}"
        hero_lead = f"Command: {tcmd} · {trows:,} rows · Version / snapshot: {tversion}"

        note_html = ""
        if tnote:
            note_cls = "ai-tool-note ai-tool-note-highlight" if tname in REQUIRED_TOOL_NOTES else "ai-tool-note"
            note_html = f'<p class="{note_cls}"><strong>Note:</strong> {esc(tnote)}</p>'

        tool_header_html = f"""
        <div class="ai-tool-header-card">
          <div class="ai-tool-header-top">
            <span class="ai-tool-cmd-chip"><code>{esc(tcmd)}</code></span>
            <span class="badge">Snapshot: {esc(tversion)}</span>
            <span class="badge">Checked: {esc(tdate)}</span>
            <span class="badge">{trows:,} rows</span>
          </div>
          <p class="ai-tool-method"><strong>Coverage method:</strong> {esc(tmethod)}</p>
          {note_html}
        </div>"""

    # Tool navigation pills
    pill_links = [
        f'<a href="./" class="platform-tab" aria-current="{"page" if is_all else "false"}">'
        f'<span>All AI tools</span><span class="tab-count">{total_rows:,}</span></a>'
    ]
    for t in all_tools:
        active = (not is_all) and (tool_meta is not None) and (t["slug"] == tool_meta["slug"])
        pill_links.append(
            f'<a href="{esc(t["slug"])}.html" class="platform-tab" aria-current="{"page" if active else "false"}">'
            f'<span>{esc(t["name"])}</span><span class="tab-count">{t["count"]:,}</span></a>'
        )
    pills_html = "\n          ".join(pill_links)

    tool_filter_section = ""
    if is_all:
        tool_filter_section = """
          <div class="rail-section">
            <div class="rail-heading">
              <h2>Tools (21)</h2>
            </div>
            <div class="category-search-wrap">
              <label for="ai-tool-search" class="sr-only">Filter tools</label>
              <input type="search" id="ai-tool-search" class="category-search-input" placeholder="Filter tools..." autocomplete="off">
            </div>
            <div class="category-list" id="ai-tool-list" role="radiogroup" aria-label="AI CLI tools">
              <!-- Rendered dynamically by ai.js -->
            </div>
          </div>"""

    mobile_tool_select = (
        '<label for="mobile-ai-tool" class="sr-only">Filter by tool</label>'
        '<select id="mobile-ai-tool" class="mobile-category-select"></select>'
        if is_all
        else ""
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(page_title)}</title>
  <meta name="description" content="{esc(meta_desc)}">
  <link rel="canonical" href="{esc(canonical)}">
  <link rel="icon" type="image/png" sizes="64x64" href="../favicon.png?v=4">
  <link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png?v=4">
  <meta name="theme-color" content="#ffffff">
  <link rel="stylesheet" href="../styles.css?v=7">
</head>
<body {body_attrs}>
  <a class="skip-link" href="#command-list">Skip to command reference</a>

  <header class="site-header">
    <div class="container header-inner">
      <div class="header-left">
        <a href="../" class="brand" aria-label="CmdAtlas Home">
          <img src="../mascot.png?v=4" alt="CmdAtlas owl mascot" width="32" height="32" class="brand-logo">
          <span class="brand-name">CmdAtlas</span>
        </a>
        <nav class="header-links" aria-label="Primary">
          <a href="../" class="nav-link">Commands</a>
          <a href="./" class="nav-link is-active">AI CLI</a>
          <a href="../credits.html" class="nav-link">About / Credits</a>
          <a href="https://github.com/allanindrajith/cmdatlas" target="_blank" rel="noopener noreferrer" class="nav-link">GitHub</a>
          <a href="https://www.buymeacoffee.com/allanidrajith" target="_blank" rel="noopener noreferrer" class="nav-link">Support</a>
        </nav>
      </div>

      <div class="header-actions">
        <a href="./" class="btn-secondary">All AI tools</a>
      </div>
    </div>
  </header>

  <main>
    <section class="hero hero-ai">
      <div class="container hero-inner">
        <img src="../mascot.png?v=4" alt="CmdAtlas owl mascot" width="72" height="72" class="hero-mascot">
        <h1>{esc(hero_h1)}</h1>
        <p class="hero-lead">{esc(hero_lead)}</p>
        {tool_header_html}

        <div class="search-pill-wrap" role="search">
          <label for="ai-search-input" class="sr-only">Search AI CLI commands and descriptions</label>
          <span class="search-icon" aria-hidden="true">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          </span>
          <input
            type="search"
            id="ai-search-input"
            class="search-input"
            placeholder="Search commands and descriptions (e.g. mcp, login, --model, /compact)..."
            autocomplete="off"
            spellcheck="false"
          >
          <kbd class="search-kbd" aria-hidden="true">/</kbd>
          <button type="button" id="ai-clear-search" class="clear-search-btn" hidden>Clear</button>
        </div>

        <nav class="platform-tabs ai-tool-tabs" aria-label="AI CLI tools">
          {pills_html}
        </nav>
      </div>
    </section>

    <section class="workspace" id="reference">
      <div class="container workspace-grid">
        <aside class="filter-rail" aria-label="Filters">
          <div class="rail-section">
            <div class="rail-heading">
              <h2>Filters</h2>
              <button type="button" id="ai-reset-filters" class="text-btn" hidden>Reset</button>
            </div>
            <div class="toggle-group" id="ai-quick-filters">
              <label class="filter-check">
                <input type="checkbox" value="has-risk">
                <span>Has risk flag</span>
                <span class="check-count" id="ai-risk-count">0</span>
              </label>
              <label class="filter-check">
                <input type="checkbox" value="hide-risky">
                <span>Hide risky commands</span>
              </label>
              <label class="filter-check">
                <input type="checkbox" value="needs-values">
                <span>Needs your values</span>
              </label>
              <label class="filter-check">
                <input type="checkbox" value="pinned">
                <span>Pinned</span>
                <span class="check-count" id="ai-pinned-count">0</span>
              </label>
            </div>
          </div>

          <div class="rail-section">
            <div class="rail-heading">
              <h2>Type</h2>
            </div>
            <div class="toggle-group" id="ai-type-filters">
              <!-- Rendered dynamically by ai.js -->
            </div>
          </div>

          <div class="rail-section">
            <div class="rail-heading">
              <h2>Public label</h2>
            </div>
            <div class="toggle-group" id="ai-label-filters">
              <!-- Rendered dynamically by ai.js -->
            </div>
          </div>
          {tool_filter_section}

          <div class="rail-section rail-shortcuts">
            <h2>Shortcuts</h2>
            <dl class="shortcut-list">
              <div><dt><kbd>/</kbd></dt><dd>Search</dd></div>
              <div><dt><kbd>Esc</kbd></dt><dd>Clear</dd></div>
            </dl>
          </div>
        </aside>

        <div class="ledger-column">
          <div class="community-notice" role="note">
            <strong>AI CLI notice:</strong>
            {esc(SITE_WIDE_NOTICE)}
            <a href="../credits.html#ai-cli">About the data &amp; licences</a>
          </div>

          <div class="ledger-toolbar">
            <p class="results-summary" id="ai-results-summary" aria-live="polite">Loading AI CLI commands…</p>
            <div class="toolbar-actions">
              {mobile_tool_select}
            </div>
          </div>

          <div id="ai-loading-state" class="loading-state">
            <p>Loading AI CLI commands…</p>
          </div>

          <div id="command-list" class="command-list">
            <!-- Command rows rendered dynamically by ai.js -->
          </div>

          <nav id="ai-pagination" class="pagination" aria-label="Pagination" hidden>
            <!-- Rendered dynamically by ai.js -->
          </nav>

          <div id="ai-empty-state" class="empty-state" hidden>
            <h3>No commands match your filters.</h3>
            <p>Try a broader search term or reset filters to browse AI CLI commands.</p>
            <button type="button" id="ai-empty-reset-btn" class="btn-primary">Reset filters</button>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container footer-inner">
      <div class="footer-links">
        <a href="../">Commands</a>
        <a href="./">AI CLI</a>
        <a href="../credits.html">About the data / Credits</a>
        <a href="https://github.com/allanindrajith/cmdatlas" target="_blank" rel="noopener noreferrer">GitHub</a>
        <a href="https://www.buymeacoffee.com/allanidrajith" target="_blank" rel="noopener noreferrer">Buy Me a Coffee</a>
        <a href="../legal.html">Privacy &amp; Terms</a>
        <a href="https://itsallan.me/" target="_blank" rel="noopener noreferrer">itsallan.me</a>
      </div>
      <p class="footer-copy">© 2026 CmdAtlas</p>
    </div>
  </footer>

  <!-- Risk / Placeholder Copy Confirmation Modal -->
  <dialog id="ai-confirm-modal" class="pdf-modal" aria-labelledby="ai-confirm-title">
    <div class="pdf-modal-inner">
      <div class="pdf-modal-header">
        <div>
          <h2 id="ai-confirm-title">Confirm before copying</h2>
          <p class="pdf-modal-sub" id="ai-confirm-sub"></p>
        </div>
        <button type="button" id="ai-close-confirm-modal" class="modal-close-btn" aria-label="Close warning dialog">&times;</button>
      </div>

      <div class="ai-confirm-warnings" id="ai-confirm-warnings"></div>

      <div class="placeholder-preview">
        <code id="ai-confirm-code"></code>
      </div>

      <p class="placeholder-note" id="ai-confirm-note"></p>

      <div class="pdf-modal-footer">
        <button type="button" id="ai-cancel-copy" class="btn-secondary">Cancel</button>
        <button type="button" id="ai-confirm-copy" class="btn-primary">Copy anyway</button>
      </div>
    </div>
  </dialog>

  <button type="button" id="back-to-top" class="back-to-top" aria-label="Back to top" hidden>
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m18 15-6-6-6 6"/></svg>
  </button>

  <div id="toast" class="toast" role="status" aria-live="polite" hidden></div>

  <script src="ai.js?v=1"></script>
</body>
</html>
"""


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    workspace_root = repo_root.parent
    xlsx_path = workspace_root / "CmdAtlas_AI_CLI_commands_audited.xlsx"

    if not xlsx_path.exists():
        print(f"ERROR: Workbook not found at {xlsx_path}", file=sys.stderr)
        return 1

    with zipfile.ZipFile(xlsx_path) as zf:
        sst: list[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            sst_root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in sst_root.findall("s:si", NS):
                sst.append("".join(t.text or "" for t in si.findall(".//s:t", NS)))

        coverage_rows = load_sheet_rows(zf, sst, "Tools Coverage")
        cmd_rows = load_sheet_rows(zf, sst, "All Commands")

    cov_headers = coverage_rows[0]
    ch = {name: i for i, name in enumerate(cov_headers)}
    coverage_by_tool: dict[str, dict] = {}
    tool_order: list[str] = []

    for row in coverage_rows[1:]:
        name = row[ch["Tool"]].strip()
        if not name:
            continue
        if name not in TOOL_SLUGS:
            raise ValueError(f"Unmapped tool in Tools Coverage: {name!r}")
        note = row[ch["Note"]].strip()
        if name in REQUIRED_TOOL_NOTES:
            note = REQUIRED_TOOL_NOTES[name]
        coverage_by_tool[name] = {
            "name": name,
            "slug": TOOL_SLUGS[name],
            "command": row[ch["Command"]].strip(),
            "coverageRows": int(row[ch["Rows"]]),
            "coverageShell": int(row[ch["Shell commands"]]),
            "coverageFlags": int(row[ch["Flags"]]),
            "coverageSlash": int(row[ch["Slash commands"]]),
            "coverageInstall": int(row[ch["Install"]]),
            "method": row[ch["Method"]].strip(),
            "version": row[ch["Version / snapshot"]].strip(),
            "note": note,
        }
        tool_order.append(name)

    headers = cmd_rows[0]
    h = {name: i for i, name in enumerate(headers)}

    all_entries: list[dict] = []
    by_tool: dict[str, list[dict]] = {TOOL_SLUGS[name]: [] for name in tool_order}
    reword_queue: list[dict] = []
    label_totals: Counter[str] = Counter()
    type_totals: Counter[str] = Counter()
    risk_total = 0
    date_checked_set: set[str] = set()
    tool_dates: dict[str, str] = {}

    for r_idx, vals in enumerate(cmd_rows[1:], start=2):
        tool_name = vals[h["Tool"]].strip()
        if tool_name not in TOOL_SLUGS:
            raise ValueError(f"Row {r_idx}: unexpected tool '{tool_name}'")
        slug = TOOL_SLUGS[tool_name]

        row_type = vals[h["Type"]].strip()
        if row_type not in VALID_TYPES:
            raise ValueError(f"Row {r_idx}: unexpected type '{row_type}'")

        public_label = vals[h["Public label"]].strip()
        if public_label not in VALID_PUBLIC_LABELS:
            raise ValueError(f"Row {r_idx}: unexpected public label '{public_label}'")

        # Rule 1: Do NOT rewrite the Command column.
        raw_command = vals[h["Command"]]
        raw_desc = vals[h["What it does"]].strip()
        license_val = vals[h["License / attribution"]].strip()
        ready_to_run = vals[h["Ready to run as-is?"]].strip()
        risk_flag = vals[h["Risk flag"]].strip()
        source_url = vals[h["Source URL"]].strip()
        version_val = vals[h["Tool version / snapshot"]].strip()
        date_checked = vals[h["Date checked"]].strip()
        platform_val = vals[h["Platform"]].strip()
        row_id = vals[h["ID"]].strip()

        date_checked_set.add(date_checked)
        tool_dates[slug] = date_checked

        # Rule 5: Descriptions © vendor docs must NOT be published verbatim;
        # "(no description in source)" stays hidden until written.
        if license_val.startswith("Descriptions © vendor docs"):
            public_summary = ""
            desc_status = "needs rewording"
            reword_queue.append(
                {
                    "id": row_id,
                    "tool": tool_name,
                    "toolSlug": slug,
                    "type": row_type,
                    "command": raw_command,
                    "descriptionStatus": "needs rewording",
                    "originalDescription": raw_desc,
                    "rewordedDescription": "",
                    "license": license_val,
                    "sourceUrl": source_url,
                }
            )
        elif raw_desc == "" or raw_desc == "(no description in source)":
            public_summary = ""
            desc_status = "missing"
            reword_queue.append(
                {
                    "id": row_id,
                    "tool": tool_name,
                    "toolSlug": slug,
                    "type": row_type,
                    "command": raw_command,
                    "descriptionStatus": "missing",
                    "originalDescription": raw_desc,
                    "rewordedDescription": "",
                    "license": license_val,
                    "sourceUrl": source_url,
                }
            )
        else:
            public_summary = raw_desc
            desc_status = "ok"

        risk_level = "caution" if risk_flag else "safe"
        if risk_flag:
            risk_total += 1

        entry = {
            "id": row_id,
            "group": slug,
            "groupLabel": tool_name,
            "tool": tool_name,
            "toolSlug": slug,
            "toolCommand": coverage_by_tool[tool_name]["command"],
            "type": row_type,
            "command": raw_command,
            "summary": public_summary,
            "descriptionStatus": desc_status,
            "platform": platform_val,
            "category": row_type,
            "readyToRun": ready_to_run,
            "riskLevel": risk_level,
            "riskFlag": risk_flag,
            "publicLabel": public_label,
            "sourceUrl": source_url,
            "version": version_val,
            "license": license_val,
            "dateChecked": date_checked,
        }

        all_entries.append(entry)
        by_tool[slug].append(entry)
        label_totals[public_label] += 1
        type_totals[row_type] += 1

    # Verify 6,005 in -> 6,005 out and compare with Tools Coverage
    mismatches = []
    manifest_tools = []
    for name in tool_order:
        cov = coverage_by_tool[name]
        slug = cov["slug"]
        items = by_tool[slug]
        t_types = Counter(x["type"] for x in items)
        t_labels = Counter(x["publicLabel"] for x in items)
        t_risks = sum(1 for x in items if x["riskFlag"])
        t_hidden_desc = sum(1 for x in items if x["descriptionStatus"] != "ok")

        if len(items) != cov["coverageRows"]:
            mismatches.append(f"{name}: All Commands={len(items)} vs Tools Coverage={cov['coverageRows']}")

        manifest_tools.append(
            {
                "name": name,
                "slug": slug,
                "command": cov["command"],
                "file": f"{slug}.json",
                "count": len(items),
                "coverageRows": cov["coverageRows"],
                "types": dict(t_types),
                "labels": dict(t_labels),
                "riskCount": t_risks,
                "hiddenDescriptions": t_hidden_desc,
                "method": cov["method"],
                "version": cov["version"],
                "note": cov["note"],
                "dateChecked": tool_dates.get(slug, "2026-11-25"),
            }
        )

    if mismatches:
        print("WARNING: Row count mismatches:", mismatches, file=sys.stderr)

    global_date = sorted(date_checked_set)[-1] if date_checked_set else "2026-11-25"
    manifest = {
        "total": len(all_entries),
        "toolCount": len(manifest_tools),
        "dateChecked": global_date,
        "notice": SITE_WIDE_NOTICE,
        "riskCount": risk_total,
        "labels": dict(label_totals),
        "types": dict(type_totals),
        "hiddenDescriptions": {
            "needsRewording": sum(1 for x in reword_queue if x["descriptionStatus"] == "needs rewording"),
            "missing": sum(1 for x in reword_queue if x["descriptionStatus"] == "missing"),
        },
        "tools": manifest_tools,
    }

    out_dirs = [
        repo_root / "data" / "ai",
        workspace_root / "website" / "data" / "ai",
    ]
    for out_dir in out_dirs:
        out_dir.mkdir(parents=True, exist_ok=True)
        for t in manifest_tools:
            slug = t["slug"]
            (out_dir / f"{slug}.json").write_text(
                json.dumps(by_tool[slug], ensure_ascii=False, separators=(",", ":")),
                encoding="utf-8",
            )
        (out_dir / "all.json").write_text(
            json.dumps(all_entries, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
        (out_dir / "index.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    # Internal rewording queue OUTSIDE website/ (never published publicly)
    internal_queue_path = repo_root / "data" / "ai-internal-reword-queue.json"
    internal_queue_path.write_text(
        json.dumps(
            {
                "note": "INTERNAL ONLY — do not copy into website/. Contains vendor-doc descriptions awaiting rewording and missing descriptions.",
                "total": len(reword_queue),
                "needsRewording": manifest["hiddenDescriptions"]["needsRewording"],
                "missing": manifest["hiddenDescriptions"]["missing"],
                "items": reword_queue,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    # Generate 22 static HTML pages under website/ai/
    ai_pages_dir = workspace_root / "website" / "ai"
    ai_pages_dir.mkdir(parents=True, exist_ok=True)

    (ai_pages_dir / "index.html").write_text(
        render_page_html(
            is_all=True,
            tool_meta=None,
            all_tools=manifest_tools,
            total_rows=len(all_entries),
            date_checked=global_date,
        ),
        encoding="utf-8",
    )

    for t in manifest_tools:
        (ai_pages_dir / f"{t['slug']}.html").write_text(
            render_page_html(
                is_all=False,
                tool_meta=t,
                all_tools=manifest_tools,
                total_rows=len(all_entries),
                date_checked=global_date,
            ),
            encoding="utf-8",
        )

    print(f"Exported {manifest['total']} AI CLI rows across {len(manifest_tools)} tools.")
    print(f"Generated 22 HTML pages in {ai_pages_dir}")
    print(f"Internal rewording queue: {len(reword_queue)} rows -> {internal_queue_path}")
    print("\nPer-tool comparison (All Commands vs Tools Coverage):")
    for t in manifest_tools:
        status = "MATCH" if t["count"] == t["coverageRows"] else "MISMATCH"
        print(f"  {t['name']:30s} ({t['slug']:18s}): {t['count']:4d} / {t['coverageRows']:4d} [{status}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
