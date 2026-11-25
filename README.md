<p align="center">
  <img src="assets/mascot.png" alt="CmdAtlas Mascot" width="96">
</p>

# CmdAtlas

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-allanidrajith-FFDD00?style=flat-square&logo=buy-me-a-coffee&logoColor=000000)](https://www.buymeacoffee.com/allanidrajith)
[![Live Web Reference](https://img.shields.io/badge/Web%20Reference-itsallan.me%2Fcmdatlas-0B5FFF?style=flat-square)](https://itsallan.me/cmdatlas/)

A structured, open-source reference of **200 Verified core CLI commands**, a **33,059-command Community collection**, and a **6,005-command AI CLI reference** across 21 AI coding & agent CLIs — **39,264 commands total**.

Built for terminal users, system administrators, developers, and homelab operators who want clean Markdown cheat sheets alongside machine-readable JSON and CSV datasets — with transparent verification labels, risk flags, and placeholder safety.

## Three-Collection Architecture

CmdAtlas keeps curated, community-sourced, and AI CLI datasets strictly separate. Community and AI CLI rows are never presented as Verified core.

### Tier 1 — Verified Core (200 commands)

Curated handbook with examples, install notes, Markdown sheets, and downloadable PDFs (`data/commands.json` + `data/commands.csv`).

| Platform Group | Commands | Markdown Sheet |
| :--- | :---: | :--- |
| **Windows** (Run, CMD, PowerShell) | 72 | [`commands/windows.md`](commands/windows.md) |
| **Linux** (Debian/Ubuntu, Fedora, Arch, Flatpak) | 68 | [`commands/linux.md`](commands/linux.md) |
| **macOS** (Terminal, `defaults`, Homebrew) | 27 | [`commands/macos.md`](commands/macos.md) |
| **Docker & Cross-Platform** (curl, SSH, Docker) | 18 | [`commands/docker-cross-platform.md`](commands/docker-cross-platform.md) |
| **Raspberry Pi OS** (vcgencmd, rpicam, GPIO) | 15 | [`commands/raspberry-pi.md`](commands/raspberry-pi.md) |
| **Total** | **200** | **168 built-in (84%) / 32 installable (16%)** |

### Tier 2 — Community Collection (33,059 commands)

Split into 6 lazy-loaded per-platform JSON files under `data/community/` (plus `data/community/index.json`).

| Platform File | Commands | Risky (`CAUTION` / `DUAL-USE`) | Has Placeholders |
| :--- | ---: | ---: | ---: |
| [`data/community/windows.json`](data/community/windows.json) *(incl. 64 DOS legacy)* | 1,414 | 67 | 882 |
| [`data/community/macos.json`](data/community/macos.json) | 1,052 | 16 | 550 |
| [`data/community/linux.json`](data/community/linux.json) | 9,041 | 152 | 6,357 |
| [`data/community/raspberry-pi.json`](data/community/raspberry-pi.json) | 88 | 1 | 20 |
| [`data/community/docker.json`](data/community/docker.json) | 400 | 13 | 216 |
| [`data/community/cross-platform.json`](data/community/cross-platform.json) | 21,064 | 201 | 15,929 |
| **Total** | **33,059** | **450** | **23,954** |

#### Public Labels (exact strings used on every community row)

| Public Label | Rows | Meaning |
| :--- | ---: | :--- |
| `Tested (Linux/Docker sandbox)` | 434 | Executed read-only in a Linux sandbox (L3, 36 rows) or binary + all flags checked against local `--help` (L2, 398 rows). |
| `Source-verified (official docs)` | 180 | Command syntax from official vendor documentation with paraphrased descriptions and source links. |
| `Community-sourced (not tested)` | 32,419 | Imported from open-source community repositories (not executed in a sandbox). |
| `Unverified (Reddit post)` | 26 | User-generated commands from public Reddit threads; unverified by definition. |

> **Platform testing note:** Only 434 rows were tested in a Linux/Docker sandbox. No Windows, macOS, or Raspberry Pi hardware was available during automated testing. Commands containing `{{placeholders}}` cannot run as-is and were not executed.

### Tier 3 — AI CLI Collection (6,005 commands across 21 tools)

Dedicated reference for modern AI coding agents, LLM runners, and model CLIs under `data/ai/` (`index.json`, `all.json`, and 21 per-tool JSON files). Live browser: [itsallan.me/cmdatlas/ai/](https://itsallan.me/cmdatlas/ai/).

| Tool | Command | Rows | Risky | File |
| :--- | :--- | ---: | ---: | :--- |
| **Hugging Face CLI (hf)** | `hf` | 1,417 | 169 | [`data/ai/huggingface-cli.json`](data/ai/huggingface-cli.json) |
| **OpenClaw** | `openclaw` | 1,330 | 65 | [`data/ai/openclaw.json`](data/ai/openclaw.json) |
| **Hermes Agent (Nous Research)** | `hermes` | 785 | 88 | [`data/ai/hermes-agent.json`](data/ai/hermes-agent.json) |
| **llama.cpp** | `llama-cli` / `llama-server` | 477 | 0 | [`data/ai/llama-cpp.json`](data/ai/llama-cpp.json) |
| **Qwen Code** | `qwen` | 267 | 4 | [`data/ai/qwen-code.json`](data/ai/qwen-code.json) |
| **Claude Code** | `claude` | 245 | 11 | [`data/ai/claude-code.json`](data/ai/claude-code.json) |
| **GitHub Copilot CLI** | `copilot` | 233 | 13 | [`data/ai/github-copilot-cli.json`](data/ai/github-copilot-cli.json) |
| **llm (Simon Willison)** | `llm` | 210 | 8 | [`data/ai/llm.json`](data/ai/llm.json) |
| **Codex CLI** | `codex` | 176 | 7 | [`data/ai/codex-cli.json`](data/ai/codex-cli.json) |
| **Aider** | `aider` | 174 | 1 | [`data/ai/aider.json`](data/ai/aider.json) |
| **OpenCode** | `opencode` | 138 | 9 | [`data/ai/opencode.json`](data/ai/opencode.json) |
| **Mistral Vibe** | `vibe` | 103 | 5 | [`data/ai/mistral-vibe.json`](data/ai/mistral-vibe.json) |
| **Kimi Code CLI** | `kimi` | 99 | 4 | [`data/ai/kimi-code-cli.json`](data/ai/kimi-code-cli.json) |
| **Antigravity CLI** | `agy` | 72 | 3 | [`data/ai/antigravity-cli.json`](data/ai/antigravity-cli.json) |
| **Gemini CLI** *(Legacy)* | `gemini` | 70 | 5 | [`data/ai/gemini-cli.json`](data/ai/gemini-cli.json) |
| **Osaurus** | `osaurus` | 64 | 4 | [`data/ai/osaurus.json`](data/ai/osaurus.json) |
| **Cursor CLI** | `agent` | 61 | 5 | [`data/ai/cursor-cli.json`](data/ai/cursor-cli.json) |
| **Ollama** | `ollama` | 32 | 3 | [`data/ai/ollama.json`](data/ai/ollama.json) |
| **DeepSeek Harness** | `dsh` | 27 | 0 | [`data/ai/deepseek-harness.json`](data/ai/deepseek-harness.json) |
| **ZCode** | `zcode` | 24 | 3 | [`data/ai/zcode.json`](data/ai/zcode.json) |
| **Windsurf** *(IDE-first)* | `windsurf` | 1 | 0 | [`data/ai/windsurf.json`](data/ai/windsurf.json) |
| **Total** | **21 tools** | **6,005** | **407** | [`data/ai/all.json`](data/ai/all.json) |

> **AI CLI freshness note:** Most AI CLI rows come from official docs or source (`3,491` rows) or Linux sandbox `--help` inspection (`2,510` rows) and have not been executed end-to-end. AI CLIs change monthly; check `dateChecked` on each tool.

## Repository Structure

```text
.
├── commands/                     # Human-readable Markdown cheat sheets (Verified core)
│   ├── windows.md
│   ├── macos.md
│   ├── linux.md
│   ├── raspberry-pi.md
│   └── docker-cross-platform.md
├── data/
│   ├── commands.json             # Verified core (200 commands)
│   ├── commands.csv              # Verified core CSV
│   ├── community/                # Community collection (33,059 commands, split by platform)
│   │   ├── index.json            # Per-platform and per-label manifest
│   │   ├── windows.json
│   │   ├── macos.json
│   │   ├── linux.json
│   │   ├── raspberry-pi.json
│   │   ├── docker.json
│   │   └── cross-platform.json
│   └── ai/                       # AI CLI collection (6,005 commands across 21 tools)
│       ├── index.json            # Per-tool manifest, counts, labels, and notes
│       ├── all.json              # Combined AI CLI dataset
│       └── <tool-slug>.json      # 21 per-tool JSON files
├── scripts/
│   ├── validate.py               # Validates Verified core + Community + AI CLI JSON files (stdlib only)
│   ├── import_community.py       # Converts audited XLSX ("All Commands") to split Community JSON files
│   └── import_ai_cli.py          # Converts audited AI CLI XLSX to JSON datasets and static tool pages
├── .github/workflows/
│   └── validate.yml              # CI validation on push and pull requests
├── CONTRIBUTING.md
└── LICENSE
```

## Schema & Metadata Flags

### Verified Core (`data/commands.json`)
- **`builtIn`** (`true` / `false`): Whether the command ships out of the box on the target OS.
- **`requiresAdmin`** (`true` / `false`): Flags commands requiring `sudo` or an elevated Administrator prompt (37 of 200 commands).
- **`riskLevel`**: `safe` (171), `caution` (28), or `deprecated` (1).

### Community Collection (`data/community/*.json`)
Retains the core schema fields (`id`, `group`, `groupLabel`, `command`, `summary`, `example`, `platform`, `category`, `install`, `builtIn`, `requiresAdmin`, `riskLevel`) and adds:
- **`publicLabel`**: Exact verification badge string (one of the 4 labels above).
- **`riskFlag`**: Raw risk annotation (`Needs sudo/admin`, `CAUTION: destructive or disruptive`, `DUAL-USE: security/pentest tool`, or empty).
- **`sourceUrl`**: Direct link to the upstream source page/file for that command.
- **`license`**: Upstream licence / attribution string preserved per row.
- **`readyToRun`**: `"Yes"` or `"No - has {{placeholders}}"` (commands starting with `"No"` have highlighted placeholders and require confirmation before copying on the web app).

## Using the Data Programmatically

```bash
# Validate Verified core + all 6 Community platform JSON files
python3 scripts/validate.py

# Filter Verified core Linux networking commands
jq '.[] | select(.group == "linux" and .category == "Networking") | {command, summary}' data/commands.json

# Filter sandbox-tested Docker commands in the Community collection
jq '.[] | select(.publicLabel == "Tested (Linux/Docker sandbox)") | {id, command, summary}' data/community/docker.json
```

## Attribution & Licences

- **tldr-pages** ([github.com/tldr-pages/tldr](https://github.com/tldr-pages/tldr)): 32,272 community rows derived from tldr-pages contributors under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes made: converted to CmdAtlas per-platform JSON schema, grouped by platform/tool, annotated with risk flags, placeholder flags, and public labels, with source links preserved.
- **trimstray/the-book-of-secret-knowledge** ([github.com/trimstray/the-book-of-secret-knowledge](https://github.com/trimstray/the-book-of-secret-knowledge)): 468 community rows under the **MIT License** (Copyright © 2018-present trimstray and contributors).
- **Official vendor documentation** (Raspberry Pi, Docker, Homebrew, Microsoft Learn): 293 rows — command syntax only with paraphrased descriptions and per-row `sourceUrl`.
- **Reddit** (user-generated content): 26 rows — commands only with paraphrased descriptions, per-row `sourceUrl`, and `Unverified (Reddit post)` label.
- **Verified core seed notice**: The initial 200-command seed dataset was compiled from a spreadsheet attributed to **technologybrief.** (Updated October 2026). Command syntax and CLI flags are factual and not copyrightable, however verbatim prose descriptions may be subject to the original author's rights.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for schema rules and how to submit new commands or corrections via Pull Request.

## Support

If CmdAtlas saved you time, you can support the project here:

<a href="https://www.buymeacoffee.com/allanidrajith" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="45"></a>
