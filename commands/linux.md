# Linux Commands (68)

Verified command reference for **Linux**.

## Categories

- [System Info](#system-info) (7)
- [Files & Navigation](#files-navigation) (3)
- [Search](#search) (4)
- [Disk & Storage](#disk-storage) (5)
- [Processes & Performance](#processes-performance) (4)
- [Networking](#networking) (10)
- [Packages](#packages) (10)
- [Services & Logs](#services-logs) (8)
- [Permissions & Users](#permissions-users) (4)
- [Archives](#archives) (4)
- [SSH & File Transfer](#ssh-file-transfer) (3)
- [Handy One-liners](#handy-one-liners) (6)

## System Info

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `inxi -Fxxxz` | Prints a full system report (CPU, GPU, RAM, kernel, drivers, disks, network) with serial numbers and IPs masked, so it's safe to share. | `inxi -Fxxxz   # inxi 3.3.37+ also accepts inxi -exxxz` | Linux | `safe` | sudo apt install inxi (Fedora: sudo dnf install inxi · Arch: sudo pacman -S inxi) |
| `fastfetch` | Shows distro, kernel, desktop, CPU, GPU, RAM and uptime beside your distro's logo; the maintained successor to the archived neofetch. | `fastfetch` | Linux | `safe` | sudo apt install fastfetch (Debian 13+, Ubuntu 26.04+ · Fedora: sudo dnf install fastfetch · Arch: sudo pacman -S fastfetch) |
| `uname -a` | Shows the kernel version, hostname and CPU architecture; uname -r prints just the kernel version. | `uname -r` | Linux | `safe` | Built in |
| `cat /etc/os-release` | Shows your distro's name and version, e.g. Ubuntu 26.04 LTS, or Debian 13 (trixie) on current Raspberry Pi OS. | `grep PRETTY_NAME /etc/os-release` | Linux | `safe` | Built in |
| `free -h` | Shows total, used and available RAM and swap in GB or MB; "available" is what apps can still use. | `free -h` | Linux | `safe` | Built in |
| `lsusb` | Lists connected USB devices, a quick check that a webcam, adapter or dev board has been detected. | `lsusb` | Linux | `safe` | Built in on most distros (else sudo apt install usbutils) |
| `sensors` | Shows CPU, GPU and motherboard temperatures plus fan speeds, useful for gaming and tracking down overheating. | `watch -n 2 sensors` | Linux | `safe` | sudo apt install lm-sensors && sudo sensors-detect (Fedora: sudo dnf install lm_sensors · Arch: sudo pacman -S lm_sensors) |

## Files & Navigation

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ls -lah` | Lists every file, hidden dotfiles included, with sizes in K/M/G, permissions, owner and last-modified date. | `ls -lah ~/Downloads` | Linux | `safe` | Built in |
| `tree -L 2` | Draws a folder's structure as a tree, here limited to two levels deep. | `tree -L 2 ~/projects` | Linux | `safe` | sudo apt install tree |
| `trash-put` | Sends files to the desktop Trash instead of deleting them permanently, so a mistake can be undone. | `trash-put old-notes.txt` | Linux | `safe` | sudo apt install trash-cli |

## Search

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `find . -name "filename"` | Searches the current folder and everything below it for a file by name; -iname ignores case and * works as a wildcard. | `find ~ -iname "*invoice*.pdf"` | Linux | `safe` | Built in |
| `find . -type f -size +500M` | Lists every file over 500 MB below the current folder, a fast way to find space hogs. | `find ~ -type f -size +1G` | Linux | `safe` | Built in |
| `grep -rni "text" .` | Searches inside every file in a folder for text, ignoring case and showing file names with line numbers. | `grep -rni "invoice" ~/Documents` | Linux | `safe` | Built in |
| `locate` | Finds files by name across the whole system instantly, using a prebuilt index. | `locate wallpaper.jpg` | Linux | `safe` | sudo apt install plocate (sudo updatedb refreshes the index) |

## Disk & Storage

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `du -sh ~/* \| sort -h` | Shows the size of each folder in your home directory, sorted so the biggest land at the bottom. | `du -sh ~/* \| sort -h` | Linux | `safe` | Built in |
| `ncdu ~` | Interactive disk-usage browser: folders are sorted biggest first and arrow keys drill down, so storage hogs stand out fast. | `sudo ncdu -x /` | Linux | `admin/sudo` | sudo apt install ncdu (Fedora: sudo dnf install ncdu · Arch: sudo pacman -S ncdu) |
| `df -h` | Shows size, used and free space for every mounted drive and partition. | `df -h /` | Linux | `safe` | Built in |
| `lsblk -f` | Lists drives and partitions with filesystem type, label, free space and mount point. | `lsblk -f` | Linux | `safe` | Built in |
| `sudo smartctl -a /dev/sda` | Reads a drive's SMART health data: overall PASSED/FAILED, reallocated sectors, power-on hours and temperature. | `sudo smartctl -a /dev/nvme0` | Linux | `admin/sudo` | sudo apt install smartmontools |

## Processes & Performance

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `htop` | Live, colorful task manager for CPU, RAM and every process; F6 sorts, F3 searches and F9 closes a program. | `htop` | Linux | `safe` | sudo apt install htop (Fedora: sudo dnf install htop · Arch: sudo pacman -S htop) |
| `btop` | Modern resource monitor with live graphs for CPU, memory, disks, network and processes. | `btop` | Linux | `safe` | sudo apt install btop |
| `pkill name` | Closes every process matching a name with no PID lookup needed; kill PID targets a single process. | `pkill firefox` | Linux | `caution` | Built in |
| `watch -n 1 command` | Reruns a command every second in full screen, handy for watching temperatures, downloads or free space. | `watch -n 1 df -h` | Linux | `safe` | Built in |

## Networking

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ip -br a` | Lists each network interface with its state and IP address, one line per interface. | `ip -br a` | Linux | `safe` | Built in |
| `hostname -I` | Prints this machine's local IP addresses, handy for SSHing in from another device. | `hostname -I` | Linux | `safe` | Built in |
| `ss -tulpn` | Lists listening ports and, with sudo, the program behind each one; the modern replacement for netstat. | `sudo ss -tulpn` | Linux | `admin/sudo` | Built in |
| `ping -c 4` | Sends four pings then stops, showing whether a host is reachable and how long replies take. | `ping -c 4 1.1.1.1` | Linux | `safe` | Built in |
| `traceroute` | Lists each network hop between you and a server, showing where a connection slows down or dies. | `traceroute example.com` | Linux | `safe` | sudo apt install traceroute |
| `mtr` | Combines traceroute and ping into a live view of packet loss at every hop, ideal for finding the bad link. | `mtr -rw example.com` | Linux | `safe` | sudo apt install mtr-tiny (Fedora/Arch: mtr) |
| `dig example.com +short` | Looks up a domain's IP address; add @1.1.1.1 to ask a specific DNS server and compare answers. | `dig @1.1.1.1 example.com +short` | Linux | `safe` | sudo apt install bind9-dnsutils (Fedora: bind-utils · Arch: bind) |
| `wget URL` | Downloads a file from a link straight into the current folder, no browser needed; -c resumes an interrupted download. | `wget -c https://example.com/file.iso` | Linux | `safe` | Built in on most distros (else sudo apt install wget) |
| `nmcli device wifi list` | Lists nearby Wi-Fi networks with signal strength, channel and security type. | `nmcli device wifi list` | Linux | `safe` | Built in on NetworkManager distros (Ubuntu, Fedora, Raspberry Pi OS) |
| `nmtui` | Text menus for joining Wi-Fi, editing connections or setting a static IP without learning nmcli syntax. | `sudo nmtui` | Linux | `admin/sudo` | Built in on NetworkManager distros (Ubuntu, Fedora, Raspberry Pi OS) |

## Packages

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `sudo apt update && sudo apt upgrade` | Refreshes the package list, then installs every available update on Debian, Ubuntu, Mint and Pop!_OS. | `sudo apt update && sudo apt upgrade -y` | Linux | `admin/sudo` | Built in |
| `sudo apt install package` | Installs a program and everything it needs from your distro's repositories; apt search keyword finds package names. | `sudo apt install vlc` | Linux | `admin/sudo` | Built in |
| `sudo apt autoremove` | Removes leftover packages that nothing installed needs anymore, freeing disk space. | `sudo apt autoremove` | Linux | `admin/sudo` `caution` | Built in |
| `sudo dnf upgrade --refresh` | Refreshes repositories and installs all updates on Fedora (dnf5 since Fedora 41). | `sudo dnf upgrade --refresh` | Linux | `admin/sudo` | Built in |
| `sudo dnf install package` | Installs a package and its dependencies on Fedora and other Red Hat-family distros; dnf search keyword finds names. | `sudo dnf install htop` | Linux | `admin/sudo` | Built in |
| `sudo pacman -Syu` | Syncs repositories and upgrades the whole system on Arch, Manjaro and EndeavourOS. | `sudo pacman -Syu` | Linux | `admin/sudo` | Built in |
| `sudo pacman -S package` | Installs a package on Arch-based distros; pacman -Ss keyword searches the repositories. | `sudo pacman -S firefox` | Linux | `admin/sudo` | Built in |
| `flatpak install flathub app.id` | Installs a sandboxed app from Flathub that runs the same on any distro. | `flatpak install flathub org.videolan.VLC` | Linux | `safe` | sudo apt install flatpak, then flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo (preinstalled on Fedora and Mint) |
| `flatpak update` | Updates every installed Flatpak app and runtime in one go. | `flatpak update -y` | Linux | `safe` | sudo apt install flatpak (preinstalled on Fedora and Mint) |
| `flatpak uninstall --unused` | Removes runtimes that no installed app uses anymore, often freeing gigabytes. | `flatpak uninstall --unused` | Linux | `caution` | sudo apt install flatpak (preinstalled on Fedora and Mint) |

## Services & Logs

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `systemctl status service` | Shows whether a service is running, since when, and its most recent log lines. | `systemctl status ssh` | Linux | `safe` | Built in |
| `sudo systemctl restart service` | Restarts a service after a config change or when it hangs. | `sudo systemctl restart NetworkManager` | Linux | `admin/sudo` `caution` | Built in |
| `sudo systemctl enable --now service` | Starts a service right away and sets it to start on every boot. | `sudo systemctl enable --now ssh` | Linux | `admin/sudo` | Built in |
| `systemctl --failed` | Lists services that failed to start, the first place to look when something breaks after boot. | `systemctl --failed` | Linux | `safe` | Built in |
| `systemd-analyze blame` | Ranks services by how long they took during boot, so you can see what slows startup. | `systemd-analyze blame \| head -15` | Linux | `safe` | Built in |
| `journalctl -b -p err` | Shows only error messages from the current boot; -b -1 shows the previous boot, useful after a crash. | `journalctl -b -1 -p err` | Linux | `safe` | Built in |
| `journalctl -u service -f` | Follows one service's log live as new lines arrive. | `journalctl -u ssh -f` | Linux | `safe` | Built in |
| `sudo journalctl --vacuum-time=2weeks` | Deletes system logs older than two weeks to reclaim space; check their size first with journalctl --disk-usage. | `journalctl --disk-usage && sudo journalctl --vacuum-time=2weeks` | Linux | `admin/sudo` | Built in |

## Permissions & Users

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `chmod +x file` | Makes a script or downloaded program executable so you can run it. | `chmod +x install.sh && ./install.sh` | Linux | `caution` | Built in |
| `chmod 644 file` | Sets permissions by number: 644 means you edit and others read, 755 adds run rights, 600 keeps it private to you. | `chmod 600 ~/.ssh/id_ed25519` | Linux | `caution` | Built in |
| `sudo chown user:group file` | Changes who owns a file or folder, fixing "permission denied" on files that were created with sudo. | `sudo chown -R $USER:$USER ~/projects` | Linux | `admin/sudo` `caution` | Built in |
| `sudo usermod -aG group $USER` | Adds you to a group, e.g. docker to run Docker without sudo or dialout for serial boards; log out and back in afterward. | `sudo usermod -aG docker $USER` | Linux | `admin/sudo` `caution` | Built in |

## Archives

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `tar -czvf archive.tar.gz folder/` | Packs a folder into one compressed .tar.gz file. | `tar -czvf docs-backup.tar.gz ~/Documents` | Linux | `safe` | Built in |
| `tar -xzvf archive.tar.gz` | Extracts a .tar.gz archive; add -C folder to extract it somewhere else. | `tar -xzvf docs-backup.tar.gz -C ~/restore` | Linux | `safe` | Built in |
| `zip -r archive.zip folder/` | Creates a .zip archive that opens natively on Windows and macOS. | `zip -r photos.zip Photos/` | Linux | `safe` | sudo apt install zip (often preinstalled) |
| `unzip file.zip -d folder` | Extracts a .zip into the folder you choose. | `unzip photos.zip -d ~/Pictures/trip` | Linux | `safe` | sudo apt install unzip (often preinstalled) |

## SSH & File Transfer

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ssh-copy-id user@host` | Copies your SSH public key to another machine so future logins need no password. | `ssh-copy-id pi@192.168.1.50` | Linux | `safe` | Built in with the OpenSSH client |
| `rsync -avh --progress source/ destination/` | Copies or syncs folders, transferring only new and changed files with a progress readout; ideal for backups. | `rsync -avh --progress ~/Photos/ /media/usb/Photos/` | Linux | `safe` | Built in on most distros (else sudo apt install rsync) |
| `rsync -avz source/ user@host:/path/` | Syncs a folder to another machine over SSH with compression; rerunning it only sends what's missing or changed. | `rsync -avz ~/projects/ pi@192.168.1.50:~/projects/` | Linux | `safe` | Built in on most distros (else sudo apt install rsync) |

## Handy One-liners

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `history \| grep keyword` | Searches your command history for anything matching a keyword; rerun a result with !number. | `history \| grep ssh` | Linux | `safe` | Built in |
| `Ctrl + R` | Searches your history as you type; press Ctrl+R again for older matches and Enter to run the one shown. | `Press Ctrl+R, then type: docker` | Linux | `safe` | Built in (bash, zsh) |
| `sudo !!` | Reruns your previous command with sudo, for when it failed with "permission denied". | `apt update   then   sudo !!` | Linux | `admin/sudo` | Built in (bash, zsh) |
| `tldr command` | Shows short, practical examples for a command instead of the full manual page. | `tldr tar` | Linux | `safe` | sudo apt install tealdeer, then tldr --update (Fedora/Arch: tealdeer) |
| `sha256sum file` | Prints a file's SHA-256 checksum so you can match it against the one on the download page. | `sha256sum debian-13-amd64-netinst.iso` | Linux | `safe` | Built in |
| `tmux` | Keeps terminal sessions running after you disconnect; detach with Ctrl+B then D, and return with tmux attach. | `tmux new -s work` | Linux | `safe` | sudo apt install tmux |
