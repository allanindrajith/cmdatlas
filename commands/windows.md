# Windows Commands (72)

Verified command reference for **Windows**.

## Categories

- [God Mode & GUID Shortcuts](#god-mode-guid-shortcuts) (8)
- [Shell Folder Shortcuts](#shell-folder-shortcuts) (5)
- [Run Box Tools](#run-box-tools) (9)
- [Disk Health & Repair](#disk-health-repair) (11)
- [System Info](#system-info) (4)
- [Packages (winget)](#packages-winget) (4)
- [Battery & Power](#battery-power) (5)
- [Networking](#networking) (10)
- [Processes & Shutdown](#processes-shutdown) (3)
- [WSL (Linux on Windows)](#wsl-linux-on-windows) (2)
- [Files & Backup](#files-backup) (1)
- [Processes & Services](#processes-services) (3)
- [Files & Downloads](#files-downloads) (3)
- [Security & Recovery](#security-recovery) (4)

## God Mode & GUID Shortcuts

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GodMode.{ED7BA470-8E54-465E-825C-99712043E01C}` | Turns a folder into God Mode (All Tasks): about 200 Control Panel settings and admin tools in one searchable window. | `Right-click the desktop > New > Folder, rename it to this exact text, press Enter; the icon turns into Control Panel` | Windows | `safe` | Built in |
| `shell:::{ED7BA470-8E54-465E-825C-99712043E01C}` | Opens the same God Mode window straight from the Run box, without creating a folder. | `Win+R, paste this, press Enter` | Windows | `safe` | Built in |
| `shell:::{D20EA4E1-3957-11d2-A40B-0C5020524153}` | Opens Windows Tools (formerly Administrative Tools): Event Viewer, Services, Disk Cleanup, Task Scheduler and more in one folder. | `Win+R, paste this, press Enter` | Windows | `safe` | Built in |
| `shell:::{7007ACC7-3202-11D1-AAD2-00805FC1270E}` | Opens Network Connections, where you can disable, re-enable or set custom DNS on Wi-Fi and Ethernet adapters. | `Win+R, paste this, press Enter` | Windows | `safe` | Built in |
| `shell:::{1206F5F1-0569-412C-8FEC-3204630DFB70}` | Opens Credential Manager to review or remove saved Windows, network-share and app sign-ins. | `Win+R, paste this, press Enter` | Windows | `safe` | Built in |
| `shell:::{025A5937-A6BE-4686-A844-36FE4BEC8B6D}` | Opens classic Power Options to switch power plans and choose what the power button and laptop lid do. | `Win+R, paste this, press Enter` | Windows | `safe` | Built in |
| `shell:::{7b81be6a-ce2b-4676-a29e-eb907a5126c5}` | Opens classic Programs and Features, the fast uninstall list that also shows install dates and sizes. | `Win+R, paste this, press Enter` | Windows | `safe` | Built in |
| `shell:::{21EC2020-3AEA-1069-A2DD-08002B30309D}` | Opens All Control Panel Items as one icon list, skipping the category view. | `Win+R, paste this, press Enter` | Windows | `safe` | Built in |

## Shell Folder Shortcuts

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `shell:startup` | Opens your Startup folder; any shortcut placed here launches automatically when you sign in. | `Win+R, type shell:startup, Enter, then drop an app shortcut in` | Windows | `safe` | Built in |
| `shell:sendto` | Opens the Send to folder so you can add your own folders and apps to the right-click Send to menu. | `Win+R, type shell:sendto, Enter` | Windows | `safe` | Built in |
| `shell:AppsFolder` | Shows every installed app, Store apps included; drag any of them onto the desktop to make a shortcut. | `Win+R, type shell:AppsFolder, Enter` | Windows | `safe` | Built in |
| `shell:appdata` | Opens your Roaming AppData folder, where many apps keep their settings, plugins and some game saves. | `Win+R, type shell:appdata, Enter` | Windows | `safe` | Built in |
| `shell:screenshots` | Opens Pictures\Screenshots, where Win+PrtScn saves full-screen captures. | `Win+R, type shell:screenshots, Enter` | Windows | `safe` | Built in |

## Run Box Tools

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `msinfo32` | Opens System Information: exact CPU, motherboard, BIOS version and date, installed RAM and whether Secure Boot is on. | `Win+R, type msinfo32, Enter` | Windows | `safe` | Built in |
| `dxdiag` | Opens the DirectX Diagnostic Tool: GPU model, video memory, driver version and display details, with a Save All Information button. | `Win+R, type dxdiag, Enter` | Windows | `safe` | Built in |
| `devmgmt.msc` | Opens Device Manager to update, roll back or reinstall drivers; yellow warning icons flag problem devices. | `Win+R, type devmgmt.msc, Enter` | Windows | `safe` | Built in |
| `diskmgmt.msc` | Opens Disk Management to see every drive and partition, change drive letters and set up a new disk. | `Win+R, type diskmgmt.msc, Enter` | Windows | `safe` | Built in |
| `resmon` | Opens Resource Monitor, showing which programs use CPU, memory, disk and network right now in more detail than Task Manager. | `Win+R, type resmon, Enter` | Windows | `safe` | Built in |
| `perfmon /rel` | Opens Reliability Monitor, a day-by-day timeline of app crashes, failed updates and hardware errors. | `Win+R, type perfmon /rel, Enter` | Windows | `safe` | Built in |
| `mdsched` | Opens Windows Memory Diagnostic, which restarts the PC and tests your RAM for faults. | `Win+R, type mdsched, Enter` | Windows | `safe` | Built in |
| `cleanmgr` | Opens Disk Cleanup; click "Clean up system files" to also remove leftover Windows Update files. | `Win+R, type cleanmgr, Enter` | Windows | `safe` | Built in |
| `sysdm.cpl` | Opens System Properties to rename the PC, turn on System Restore, trim visual effects and edit environment variables. | `Win+R, type sysdm.cpl, Enter` | Windows | `safe` | Built in |

## Disk Health & Repair

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `wmic diskdrive get model,status` | Lists each drive's model and health status (OK, Pred Fail); WMIC was removed from Windows 11 24H2+ in August 2026, so use Get-PhysicalDisk there. | `wmic diskdrive get model,status` | Windows CMD | `deprecated` | Built in on Windows 10 only (removed from Windows 11 24H2 and later) |
| `chkdsk C:` | Read-only check of drive C:'s file system that reports errors without fixing them; run Command Prompt as admin. | `chkdsk C:` | Windows CMD | `admin/sudo` | Built in |
| `chkdsk C: /f` | Fixes file-system errors on the drive; because C: is in use, it offers to run at the next restart. | `chkdsk C: /f` | Windows CMD | `caution` | Built in |
| `chkdsk C: /r` | Does everything /f does, plus scans every sector for bad spots and recovers readable data; can take hours on a large hard drive. | `chkdsk C: /r` | Windows CMD | `caution` | Built in |
| `chkdsk C: /scan` | Scans the drive online without locking it, so you can keep working while it checks for file-system errors. | `chkdsk C: /scan` | Windows CMD | `safe` | Built in |
| `DISM /Online /Cleanup-Image /RestoreHealth` | Repairs the Windows component store using Windows Update; run it before sfc /scannow from an admin prompt. | `DISM /Online /Cleanup-Image /RestoreHealth` | Windows CMD | `admin/sudo` | Built in |
| `sfc /scannow` | Scans protected Windows system files and replaces corrupted ones; run it after DISM, as admin. | `sfc /scannow` | Windows CMD | `admin/sudo` | Built in |
| `DISM /Online /Cleanup-Image /StartComponentCleanup` | Clears superseded update files out of the Windows component store to free disk space; run as admin. | `DISM /Online /Cleanup-Image /StartComponentCleanup` | Windows CMD | `admin/sudo` `caution` | Built in |
| `Get-PhysicalDisk \| Select FriendlyName, HealthStatus, OperationalStatus` | The modern replacement for wmic diskdrive: lists each drive with its health (Healthy, Warning, Unhealthy) and operational status. | `Get-PhysicalDisk \| Select FriendlyName, MediaType, HealthStatus, OperationalStatus` | Windows PowerShell | `safe` | Built in |
| `Get-PhysicalDisk \| Get-StorageReliabilityCounter` | Shows SMART-style counters for each drive: temperature, wear, read/write errors and power-on hours; run PowerShell as admin. | `Get-PhysicalDisk \| Get-StorageReliabilityCounter \| Select-Object DeviceId, Temperature, Wear, ReadErrorsTotal, WriteErrorsTotal, PowerOnHours` | Windows PowerShell | `admin/sudo` | Built in |
| `Optimize-Volume -DriveLetter C` | Runs TRIM on an SSD or defragments a hard drive, the same job as Defragment and Optimize Drives; run as admin. | `Optimize-Volume -DriveLetter C -Verbose` | Windows PowerShell | `admin/sudo` `caution` | Built in |

## System Info

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `systeminfo` | Lists Windows edition and build, install date, last boot time, RAM, BIOS version and installed updates. | `systeminfo \| findstr /B /C:"OS Name" /C:"OS Version"` | Windows CMD | `safe` | Built in |
| `manage-bde -status` | Shows whether each drive is BitLocker-encrypted and how far encryption has progressed; run as admin. | `manage-bde -status C:` | Windows CMD | `admin/sudo` | Built in |
| `Get-ComputerInfo` | Dumps detailed Windows, BIOS and hardware info; pick the fields you want with Select-Object. | `Get-ComputerInfo \| Select-Object OsName, OsVersion, CsModel, BiosSMBIOSBIOSVersion` | Windows PowerShell | `safe` | Built in |
| `Get-CimInstance Win32_BIOS \| Select-Object SerialNumber` | Shows the PC's serial number for warranty lookups, replacing the removed wmic bios get serialnumber. | `Get-CimInstance Win32_BIOS \| Select-Object SerialNumber` | Windows PowerShell | `safe` | Built in |

## Packages (winget)

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `winget search name` | Searches the Windows Package Manager catalog and shows each app's exact ID. | `winget search vlc` | Windows CMD | `safe` | Built in (Windows 10/11, via App Installer) |
| `winget install --id ID -e` | Installs an app by its exact ID, with no website or installer hunting. | `winget install --id Mozilla.Firefox -e` | Windows CMD | `safe` | Built in (Windows 10/11, via App Installer) |
| `winget upgrade --all` | Updates every app winget can see; run plain winget upgrade first to preview the list. | `winget upgrade --all --include-unknown` | Windows CMD | `safe` | Built in (Windows 10/11, via App Installer) |
| `winget export -o apps.json` | Saves a list of your installed apps; on a new PC, winget import -i apps.json reinstalls them all. | `winget export -o apps.json` | Windows CMD | `safe` | Built in (Windows 10/11, via App Installer) |

## Battery & Power

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `powercfg /batteryreport` | Saves an HTML battery report: design vs. current full-charge capacity, cycle count and usage history. | `powercfg /batteryreport /output "%USERPROFILE%\battery.html"` | Windows CMD | `safe` | Built in |
| `powercfg /sleepstudy` | Builds an HTML report of recent Modern Standby sleep sessions, showing what drained the battery while the lid was shut. | `powercfg /sleepstudy /duration 7` | Windows CMD | `safe` | Built in (Modern Standby laptops) |
| `powercfg /energy` | Watches the PC for 60 seconds, then writes energy-report.html listing power and battery-life problems; run as admin. | `powercfg /energy` | Windows CMD | `admin/sudo` | Built in |
| `powercfg /requests` | Lists apps and drivers currently keeping the screen on or blocking sleep; run as admin. | `powercfg /requests` | Windows CMD | `admin/sudo` | Built in |
| `powercfg /lastwake` | Shows what woke the PC from its last sleep, such as a mouse, network adapter or wake timer. | `powercfg /lastwake` | Windows CMD | `safe` | Built in |

## Networking

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ipconfig /all` | Shows every adapter's IP address, MAC address, gateway, DNS servers and DHCP lease. | `ipconfig /all` | Windows CMD | `safe` | Built in |
| `ipconfig /flushdns` | Clears the DNS cache, often fixing sites that won't load after a DNS or hosting change. | `ipconfig /flushdns` | Windows CMD | `safe` | Built in |
| `ping -t` | Pings nonstop until Ctrl+C, handy for spotting Wi-Fi dropouts; plain ping sends four and stops. | `ping -t 1.1.1.1` | Windows CMD | `safe` | Built in |
| `tracert` | Lists every hop between your PC and a site, showing where a connection slows down or breaks. | `tracert example.com` | Windows CMD | `safe` | Built in |
| `nslookup` | Looks up a domain's IP address; add a DNS server's address to compare its answer. | `nslookup example.com 1.1.1.1` | Windows CMD | `safe` | Built in |
| `netstat -ano` | Lists all connections and listening ports with the process ID behind each, which you can match in Task Manager. | `netstat -ano \| findstr LISTENING` | Windows CMD | `safe` | Built in |
| `netsh wlan show profile name="WiFiName" key=clear` | Reveals a saved Wi-Fi network's password under Key Content; netsh wlan show profiles lists saved names. Run as admin. | `netsh wlan show profile name="HomeWiFi" key=clear` | Windows CMD | `admin/sudo` `caution` | Built in |
| `netsh wlan show wlanreport` | Builds an HTML report of the last three days of Wi-Fi sessions and disconnects; run as admin. | `netsh wlan show wlanreport, then open C:\ProgramData\Microsoft\Windows\WlanReport\wlan-report-latest.html` | Windows CMD | `admin/sudo` | Built in |
| `Test-NetConnection host -Port 443` | Checks whether a server and a specific port are reachable, with ping and route details. | `Test-NetConnection example.com -Port 443` | Windows PowerShell | `safe` | Built in |
| `Resolve-DnsName example.com` | Looks up DNS records for a domain; -Server chooses which DNS server to ask. | `Resolve-DnsName example.com -Server 1.1.1.1` | Windows PowerShell | `safe` | Built in |

## Processes & Shutdown

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `tasklist` | Lists running processes with their process IDs and memory use. | `tasklist \| findstr chrome` | Windows CMD | `safe` | Built in |
| `taskkill /IM name.exe /F` | Force-closes a frozen program by its process name. | `taskkill /IM notepad.exe /F` | Windows CMD | `caution` | Built in |
| `shutdown /r /o /t 0` | Restarts straight into Advanced Startup for Safe Mode, System Restore or booting from a USB drive. | `shutdown /r /o /t 0` | Windows CMD | `caution` | Built in |

## WSL (Linux on Windows)

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `wsl --install` | Installs Windows Subsystem for Linux with Ubuntu by default (-d picks another distro); run as admin and restart when asked. | `wsl --install -d Debian` | Windows CMD | `admin/sudo` | Built in |
| `wsl -l -v` | Lists installed Linux distros, whether each is running and which WSL version it uses. | `wsl -l -v` | Windows CMD | `safe` | Built in |

## Files & Backup

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `robocopy source destination /E` | Copies a folder and all its subfolders, skipping files that haven't changed; ideal for repeat backups to an external drive. | `robocopy C:\Users\Me\Pictures D:\Backup\Pictures /E /R:2 /W:2` | Windows CMD | `safe` | Built in |

## Processes & Services

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Get-Process \| Sort-Object CPU -Descending \| Select-Object -First 10` | Lists the ten processes that have used the most CPU time since they started. | `Get-Process \| Sort-Object CPU -Descending \| Select-Object -First 10` | Windows PowerShell | `safe` | Built in |
| `Restart-Service -Name Spooler` | Restarts the Print Spooler, the quick fix for a stuck print queue; run as admin. | `Restart-Service -Name Spooler` | Windows PowerShell | `admin/sudo` `caution` | Built in |
| `Get-PnpDevice -PresentOnly \| Where-Object Status -ne 'OK'` | Lists connected devices with driver or hardware problems, the same ones Device Manager flags. | `Get-PnpDevice -PresentOnly \| Where-Object Status -ne 'OK'` | Windows PowerShell | `safe` | Built in |

## Files & Downloads

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Get-FileHash file -Algorithm SHA256` | Prints a file's SHA-256 hash to match against the checksum on the download page. | `Get-FileHash .\Win11.iso -Algorithm SHA256` | Windows PowerShell | `safe` | Built in |
| `Get-ChildItem -Recurse -File \| Sort-Object Length -Descending \| Select-Object -First 10 FullName, Length` | Finds the ten largest files under the current folder, Windows' answer to du for tracking down space hogs. | `cd $HOME; Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue \| Sort-Object Length -Descending \| Select-Object -First 10 FullName, Length` | Windows PowerShell | `safe` | Built in |
| `Invoke-WebRequest -Uri URL -OutFile file` | Downloads a file from a URL, PowerShell's built-in answer to wget. | `Invoke-WebRequest -Uri https://example.com/file.zip -OutFile file.zip` | Windows PowerShell | `safe` | Built in |

## Security & Recovery

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Get-MpComputerStatus` | Shows Microsoft Defender's status: whether real-time protection is on, when it last scanned and how fresh its virus definitions are. | `Get-MpComputerStatus \| Select-Object RealTimeProtectionEnabled, AntivirusSignatureLastUpdated, QuickScanEndTime` | Windows PowerShell | `safe` | Built in |
| `Start-MpScan -ScanType QuickScan` | Runs a Microsoft Defender quick scan from the command line; use FullScan to check every file. | `Start-MpScan -ScanType FullScan` | Windows PowerShell | `safe` | Built in |
| `Checkpoint-Computer -Description "name"` | Creates a System Restore point before a risky change; needs admin and System Protection on, allows one per 24 hours, Windows PowerShell 5.1 only. | `Checkpoint-Computer -Description "Before driver update"` | Windows PowerShell | `admin/sudo` | Built in |
| `Get-WinEvent -FilterHashtable @{LogName='System'; Level=2} -MaxEvents 20` | Shows the 20 most recent errors in the System event log without opening Event Viewer. | `Get-WinEvent -FilterHashtable @{LogName='System'; Level=2} -MaxEvents 20` | Windows PowerShell | `safe` | Built in |
