# Raspberry Pi Commands (15)

Verified command reference for **Raspberry Pi**.

## Categories

- [Temperature & Power](#temperature-power) (3)
- [Setup & Updates](#setup-updates) (3)
- [System Info](#system-info) (3)
- [Camera](#camera) (3)
- [GPIO](#gpio) (3)

## Temperature & Power

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `vcgencmd measure_temp` | Shows the Pi's processor temperature; the CPU starts throttling between 80 and 85°C. | `watch -n 2 vcgencmd measure_temp` | Raspberry Pi OS | `safe` | Built in |
| `vcgencmd get_throttled` | Flags power and heat trouble: throttled=0x0 is healthy, while 0x50000 means under-voltage and throttling happened since boot, so check the power supply. | `vcgencmd get_throttled` | Raspberry Pi OS | `safe` | Built in |
| `vcgencmd measure_clock arm` | Shows the current CPU clock speed in Hz, a quick check of whether the Pi is running at full speed. | `vcgencmd measure_clock arm` | Raspberry Pi OS | `safe` | Built in |

## Setup & Updates

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `sudo raspi-config` | Text menu for enabling SSH, VNC, I2C, SPI and serial, and setting hostname, Wi-Fi country, locale and boot options. | `sudo raspi-config` | Raspberry Pi OS | `admin/sudo` | Built in |
| `sudo apt update && sudo apt full-upgrade` | Raspberry Pi's recommended update; full-upgrade also handles the dependency changes Pi OS ships more often than Debian. | `sudo apt update && sudo apt full-upgrade -y` | Raspberry Pi OS | `admin/sudo` | Built in |
| `sudo rpi-eeprom-update` | Checks whether newer bootloader firmware is available on a Pi 4 or Pi 5; add -a to install it at the next reboot. | `sudo rpi-eeprom-update -a` | Raspberry Pi OS | `admin/sudo` `caution` | Built in |

## System Info

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `cat /etc/rpi-issue` | Shows which Raspberry Pi OS image you installed and its build date; cat /etc/os-release gives the Debian version. | `cat /etc/rpi-issue` | Raspberry Pi OS | `safe` | Built in |
| `cat /proc/device-tree/model` | Prints the exact board model and revision, e.g. Raspberry Pi 5 Model B Rev 1.0. | `cat /proc/device-tree/model` | Raspberry Pi OS | `safe` | Built in |
| `dpkg --print-architecture` | Shows whether you're running 64-bit (arm64) or 32-bit (armhf) Raspberry Pi OS, which decides what software you can install. | `dpkg --print-architecture` | Raspberry Pi OS | `safe` | Built in |

## Camera

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `rpicam-hello --list-cameras` | Lists connected camera modules and their sensor modes; plain rpicam-hello opens a live preview. | `rpicam-hello -t 0` | Raspberry Pi OS | `safe` | Built in (Bookworm and later; formerly libcamera-hello) |
| `rpicam-still -o photo.jpg` | Takes a full-resolution photo with the camera module; it replaced libcamera-still and raspistill. | `rpicam-still -o photo.jpg` | Raspberry Pi OS | `safe` | Built in (Bookworm and later) |
| `rpicam-vid -t 10s -o video.mp4` | Records 10 seconds of video; a Pi 5 writes MP4 directly, while older boards need --codec libav. | `rpicam-vid -t 10s --codec libav -o video.mp4` | Raspberry Pi OS | `safe` | Built in (Bookworm and later) |

## GPIO

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pinctrl get 17` | Shows a GPIO pin's mode and level; plain pinctrl lists every pin. It replaces the old raspi-gpio tool. | `pinctrl get 17` | Raspberry Pi OS | `safe` | Built in (Bookworm and later) |
| `pinctrl set 17 op dh` | Sets GPIO17 as an output and drives it high (3.3 V), e.g. to light an LED; dl drives it low again. | `pinctrl set 17 op dl` | Raspberry Pi OS | `caution` | Built in (Bookworm and later) |
| `pinout` | Draws your board's GPIO header in the terminal with every pin number, power pin and ground pin labeled. | `pinout` | Raspberry Pi OS | `safe` | Built in on most images (else sudo apt install python3-gpiozero) |
