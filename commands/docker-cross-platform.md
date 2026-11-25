# Docker & Cross-Platform Commands (18)

Verified command reference for **Docker & Cross-Platform**.

## Categories

- [Networking](#networking) (3)
- [SSH & File Transfer](#ssh-file-transfer) (4)
- [Docker](#docker) (11)

## Networking

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `curl -I https://example.com` | Fetches only a page's headers (status code, server, redirects), a quick check of whether a site is up. | `curl -I https://example.com` | Cross-platform | `safe` | Built in (Windows 10/11 as curl.exe, macOS, most Linux) |
| `curl -L -O URL` | Downloads a file under its original name, following redirects; in Windows PowerShell type curl.exe. | `curl -L -O https://example.com/file.zip` | Cross-platform | `safe` | Built in (Windows 10/11 as curl.exe, macOS, most Linux) |
| `curl ifconfig.me` | Prints your public IP address, the one websites see. | `curl ifconfig.me` | Cross-platform | `safe` | Built in (Windows 10/11 as curl.exe, macOS, most Linux) |

## SSH & File Transfer

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ssh user@host` | Logs into another computer's terminal securely, such as a Raspberry Pi or home server. | `ssh pi@192.168.1.50` | Cross-platform | `safe` | Built in (Windows 10/11, macOS, most Linux) |
| `ssh-keygen -t ed25519` | Creates a modern SSH key pair for password-free, more secure logins. | `ssh-keygen -t ed25519 -C "laptop"` | Cross-platform | `safe` | Built in (Windows 10/11, macOS, most Linux) |
| `scp file user@host:path` | Copies files to or from another machine over SSH. | `scp photo.jpg pi@192.168.1.50:~/Pictures/` | Cross-platform | `safe` | Built in (Windows 10/11, macOS, most Linux) |
| `ssh -L 8080:localhost:80 user@host` | Tunnels a remote port to your machine, so a device's web page opens at localhost:8080 in your browser. | `ssh -L 8080:localhost:80 pi@192.168.1.50` | Cross-platform | `safe` | Built in (Windows 10/11, macOS, most Linux) |

## Docker

| Command | What it does | Example | Platform | Flags | Install |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `docker run hello-world` | Confirms Docker is installed and working by running a tiny test container. | `docker run hello-world` | Cross-platform | `safe` | Docker Desktop (Windows, macOS) · Linux/Pi: curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh |
| `docker run -d --name web -p 8080:80 nginx` | Starts a container in the background and maps its port 80 to localhost:8080 on your machine. | `docker run -d --name web -p 8080:80 nginx` | Cross-platform | `safe` | Docker Desktop (Windows, macOS) · Linux/Pi: curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh |
| `docker ps -a` | Lists containers with their status, ports and names; drop -a to see only running ones. | `docker ps -a` | Cross-platform | `safe` | Docker Desktop (Windows, macOS) · Linux/Pi: curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh |
| `docker logs -f name` | Streams a container's log output live. | `docker logs -f web` | Cross-platform | `safe` | Docker Desktop (Windows, macOS) · Linux/Pi: curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh |
| `docker exec -it name sh` | Opens a shell inside a running container so you can look around or fix things. | `docker exec -it web sh` | Cross-platform | `safe` | Docker Desktop (Windows, macOS) · Linux/Pi: curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh |
| `docker compose up -d` | Starts every service in a compose.yaml in the background, the standard way to self-host apps. | `docker compose up -d` | Cross-platform | `safe` | Docker Desktop (Windows, macOS) · Linux/Pi: curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh |
| `docker compose down` | Stops and removes a stack's containers and network; named volumes and their data are kept. | `docker compose down` | Cross-platform | `caution` | Docker Desktop (Windows, macOS) · Linux/Pi: curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh |
| `docker compose pull` | Downloads newer images for a stack; follow with docker compose up -d to switch over. | `docker compose pull && docker compose up -d` | Cross-platform | `safe` | Docker Desktop (Windows, macOS) · Linux/Pi: curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh |
| `docker system df` | Shows how much disk space images, containers, volumes and build cache are using. | `docker system df` | Cross-platform | `safe` | Docker Desktop (Windows, macOS) · Linux/Pi: curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh |
| `docker image prune` | Deletes dangling (untagged) images after asking for confirmation, reclaiming disk space. | `docker image prune` | Cross-platform | `caution` | Docker Desktop (Windows, macOS) · Linux/Pi: curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh |
| `docker run --rm -it ubuntu bash` | Opens a throwaway Ubuntu shell that disappears when you exit, perfect for testing commands safely. | `docker run --rm -it ubuntu bash` | Cross-platform | `safe` | Docker Desktop (Windows, macOS) · Linux/Pi: curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh |
