<p align="center">
  <img src="assets/mascot.png" alt="CmdAtlas Mascot" width="96">
</p>

# CmdAtlas

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-allanidrajith-FFDD00?style=flat-square&logo=buy-me-a-coffee&logoColor=000000)](https://www.buymeacoffee.com/allanidrajith)
[![Live Web Reference](https://img.shields.io/badge/Web%20Reference-itsallan.me%2Fcmdatlas-0B5FFF?style=flat-square)](https://itsallan.me/cmdatlas/)

A structured, community-maintainable reference of **200 verified command-line tools and shortcuts** across Windows, macOS, Linux, Raspberry Pi OS, and Docker/Cross-Platform environments.

Built for terminal users, system administrators, developers, and homelab operators who want clean Markdown cheat sheets alongside machine-readable JSON and CSV datasets.

> **Important Attribution & Licensing Notice**
> The initial 200-command seed dataset was compiled from a spreadsheet attributed to **technologybrief.** (Updated October 2026). Command syntax and CLI flags are factual and not copyrightable, **however verbatim prose descriptions may be subject to the original author's rights**. Before publishing this repository publicly under an open-source license, either obtain permission/confirm the upstream license or rewrite the `summary` field in your own words.

## Dataset Summary

| Platform Group | Commands | Markdown Sheet |
| :--- | :---: | :--- |
| **Windows** (Run, CMD, PowerShell) | 72 | [`commands/windows.md`](commands/windows.md) |
| **Linux** (Debian/Ubuntu, Fedora, Arch, Flatpak) | 68 | [`commands/linux.md`](commands/linux.md) |
| **macOS** (Terminal, `defaults`, Homebrew) | 27 | [`commands/macos.md`](commands/macos.md) |
| **Docker & Cross-Platform** (curl, SSH, Docker) | 18 | [`commands/docker-cross-platform.md`](commands/docker-cross-platform.md) |
| **Raspberry Pi OS** (vcgencmd, rpicam, GPIO) | 15 | [`commands/raspberry-pi.md`](commands/raspberry-pi.md) |
| **Total** | **200** | **168 built-in (84%) / 32 installable (16%)** |

## Repository Structure

```text
.
├── commands/                     # Human-readable Markdown cheat sheets by OS
│   ├── windows.md
│   ├── macos.md
│   ├── linux.md
│   ├── raspberry-pi.md
│   └── docker-cross-platform.md
├── data/                         # Machine-readable datasets
│   ├── commands.json             # Full structured schema with risk & admin flags
│   └── commands.csv              # Flat CSV for spreadsheets & scripts
├── scripts/
│   └── validate.py               # Schema, duplicate & parity validator (stdlib only)
├── .github/workflows/
│   └── validate.yml              # CI validation on push and pull requests
├── CONTRIBUTING.md
└── LICENSE
```

## Metadata Flags

Every entry in `data/commands.json` and `data/commands.csv` includes:

- **`builtIn`** (`true` / `false`): Whether the command ships out of the box on the target OS.
- **`requiresAdmin`** (`true` / `false`): Flags commands requiring `sudo` or an elevated Administrator prompt (37 of 200 commands).
- **`riskLevel`**:
  - `safe` (171): Read-only inspection or non-destructive utility.
  - `caution` (28): Modifies system state, permissions, processes, services, or deletes data/logs/images.
  - `deprecated` (1): `wmic diskdrive` (removed in Windows 11 24H2+; use `Get-PhysicalDisk`).

## Using the Data Programmatically

```bash
# Validate dataset integrity locally
python3 scripts/validate.py

# Filter Linux networking commands with jq
jq '.[] | select(.group == "linux" and .category == "Networking") | {command, summary}' data/commands.json
```

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for schema rules and how to submit new commands or corrections via Pull Request.

## Support

If CmdAtlas saved you time, you can support the project here:

<a href="https://www.buymeacoffee.com/allanidrajith" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="45"></a>
