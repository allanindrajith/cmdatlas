# Contributing to CmdAtlas

Contributions are welcome! To keep this index accurate, safe, and machine-readable, follow these rules when opening a pull request.

## Adding or Updating a Command

1. Edit `data/commands.json` and keep `data/commands.csv` and the corresponding `commands/<group>.md` file in sync.
2. Every entry in `data/commands.json` must include all required fields:
   - `id`: Unique identifier (`win-073`, `mac-028`, `lin-069`, `rpi-016`, `xplat-019`).
   - `group`: One of `windows`, `macos`, `linux`, `raspberry-pi`, `docker-cross-platform`.
   - `groupLabel`: Display name of the group.
   - `command`: Exact command template or shortcut.
   - `summary`: Plain-English explanation written in your own words (no copied third-party prose).
   - `example`: Concrete, runnable example.
   - `platform`: Specific shell/OS (e.g., `Windows CMD`, `Windows PowerShell`, `macOS`, `Linux`, `Raspberry Pi OS`, `Cross-platform`).
   - `category`: Logical topic category.
   - `install`: `Built in` or exact package-manager install instructions.
   - `builtIn`: Boolean.
   - `requiresAdmin`: Boolean (`true` if `sudo` or elevated Administrator prompt is needed).
   - `riskLevel`: One of `safe`, `caution`, or `deprecated`.
3. Never add destructive one-liners without setting `"riskLevel": "caution"`.
4. Run the validator before opening a PR:

```bash
python3 scripts/validate.py
```

All pull requests are automatically checked by GitHub Actions.
