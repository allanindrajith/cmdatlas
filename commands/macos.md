# macOS Commands (27)

Verified command reference for **macOS**.

## Categories

- [Power & Sleep](#power-sleep) (5)
- [Networking](#networking) (3)
- [Search & Files](#search-files) (5)
- [Screenshots](#screenshots) (3)
- [Finder & Dock Tweaks](#finder-dock-tweaks) (5)
- [System Info & Maintenance](#system-info-maintenance) (5)
- [Packages (Homebrew)](#packages-homebrew) (1)

## Power & Sleep

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `caffeinate -d` | Keeps the display and Mac awake until you press Ctrl+C; -t sets a time limit in seconds. | `caffeinate -d -t 3600` | macOS | `safe` | Built in |
| `caffeinate -i command` | Stops the Mac idle-sleeping only while a long command runs, then lets it sleep normally. | `caffeinate -i rsync -a ~/Projects/ /Volumes/Backup/Projects/` | macOS | `safe` | Built in |
| `pmset -g batt` | Shows battery percentage, whether it's charging and the estimated time remaining. | `pmset -g batt` | macOS | `safe` | Built in |
| `pmset -g assertions` | Lists what is currently preventing sleep, such as a video call, download or app. | `pmset -g assertions` | macOS | `safe` | Built in |
| `sudo pmset -a lowpowermode 1` | Turns Low Power Mode on for both battery and charger; 0 turns it back off. | `sudo pmset -a lowpowermode 0` | macOS | `admin/sudo` | Built in |

## Networking

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `networkQuality` | Apple's built-in speed test: download and upload speed plus responsiveness under load, no website needed. | `networkQuality -v` | macOS | `safe` | Built in (macOS 12 and later) |
| `ipconfig getifaddr en0` | Prints your Mac's local IP address on Wi-Fi, which is en0 on most Macs. | `ipconfig getifaddr en0` | macOS | `safe` | Built in |
| `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder` | Flushes the DNS cache when websites fail to load after a DNS or network change. | `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder` | macOS | `admin/sudo` | Built in |

## Search & Files

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `mdfind "text"` | Runs a Spotlight search from Terminal across file names and contents; -onlyin limits it to one folder. | `mdfind -onlyin ~/Documents "tax return"` | macOS | `safe` | Built in |
| `mdfind -name filename` | Finds files by name only, instantly, using the Spotlight index. | `mdfind -name invoice.pdf` | macOS | `safe` | Built in |
| `pbcopy` | Copies a command's output straight to the clipboard; pbpaste pastes it back out. | `cat ~/.ssh/id_ed25519.pub \| pbcopy` | macOS | `safe` | Built in |
| `sips -s format jpeg photo.heic --out photo.jpg` | Converts an image to another format, here iPhone HEIC to JPG, with the Mac's built-in image tool. | `sips -s format jpeg IMG_0420.heic --out IMG_0420.jpg` | macOS | `safe` | Built in |
| `shasum -a 256 file` | Prints a download's SHA-256 checksum to compare with the one the publisher lists. | `shasum -a 256 ~/Downloads/app.dmg` | macOS | `safe` | Built in |

## Screenshots

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `defaults write com.apple.screencapture location ~/Pictures/Screenshots` | Saves screenshots to a folder of your choice instead of cluttering the Desktop; create the folder first. | `mkdir -p ~/Pictures/Screenshots && defaults write com.apple.screencapture location ~/Pictures/Screenshots && killall SystemUIServer` | macOS | `caution` | Built in |
| `defaults write com.apple.screencapture type jpg` | Switches the screenshot format from PNG to smaller JPG files; heic, pdf and tiff also work. | `defaults write com.apple.screencapture type jpg && killall SystemUIServer` | macOS | `caution` | Built in |
| `defaults write com.apple.screencapture disable-shadow -bool true` | Removes the large drop shadow from window screenshots. | `defaults write com.apple.screencapture disable-shadow -bool true && killall SystemUIServer` | macOS | `caution` | Built in |

## Finder & Dock Tweaks

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `defaults write com.apple.finder AppleShowAllFiles -bool true` | Always shows hidden files in Finder; Cmd+Shift+. toggles them temporarily instead. | `defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder` | macOS | `caution` | Built in |
| `defaults write com.apple.finder ShowPathbar -bool true` | Adds a path bar to the bottom of Finder windows showing exactly which folder you're in. | `defaults write com.apple.finder ShowPathbar -bool true && killall Finder` | macOS | `caution` | Built in |
| `defaults write NSGlobalDomain AppleShowAllExtensions -bool true` | Shows every file extension in Finder, so a file like invoice.pdf.app can't pass itself off as a PDF. | `defaults write NSGlobalDomain AppleShowAllExtensions -bool true && killall Finder` | macOS | `caution` | Built in |
| `defaults write com.apple.dock autohide-delay -float 0` | Makes an auto-hiding Dock appear instantly instead of after a short pause. | `defaults write com.apple.dock autohide-delay -float 0 && killall Dock` | macOS | `caution` | Built in |
| `defaults delete domain key` | Undoes any defaults tweak by removing it, which restores the macOS default. | `defaults delete com.apple.dock autohide-delay && killall Dock` | macOS | `caution` | Built in |

## System Info & Maintenance

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `sw_vers` | Shows the macOS version and build number. | `sw_vers` | macOS | `safe` | Built in |
| `system_profiler SPHardwareDataType` | Shows your Mac's model, chip, memory, serial number and firmware version. | `system_profiler SPHardwareDataType` | macOS | `safe` | Built in |
| `softwareupdate -l` | Lists available macOS updates; sudo softwareupdate -i -a installs all of them. | `sudo softwareupdate -i -a` | macOS | `admin/sudo` | Built in |
| `diskutil info disk0` | Shows details on the internal drive, including its SMART status (Verified means healthy). | `diskutil info disk0 \| grep SMART` | macOS | `safe` | Built in |
| `tmutil startbackup` | Starts a Time Machine backup right now; tmutil latestbackup shows where the last one is saved. | `tmutil startbackup` | macOS | `safe` | Built in |

## Packages (Homebrew)

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `brew install name` | Installs command-line tools and apps from Homebrew, the Mac's most popular package manager; brew upgrade updates them all. | `brew install btop` | macOS | `safe` | /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" |
