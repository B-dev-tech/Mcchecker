# 🎮 Minecraft Server Checker

**Version:** 1.7 Stable  
**Author:** B-dev  

A simple and interactive **Minecraft server checker** CLI tool.  
Check the status, player count, ping, and open TCP/UDP ports of a Minecraft server.  
Supports **Java Edition** and provides optional colorful output using `rich`.

---

## ✨ Features

- ✅ Interactive CLI (`Mcchecker start`)  
- ✅ Optional flags:
  - `--rich` → Pretty colored output  
  - `--version` → Show version info  
- ✅ Check **Minecraft server status**  
- ✅ Show **Host name**, **Server name**, **Minecraft server IP**  
- ✅ Display **Operating system** of the machine running the checker  
- ✅ Scan **TCP/UDP ports** (default: 25565, 19132, 11, 21)  
- ✅ Works on **Linux (Termux), Windows, macOS**  

---

## 🛠 Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/minecraft-server-checker.git
cd minecraft-server-checker

2. Install dependencies:



pip install -r requirements.txt


---

🚀 Usage

Start interactive checker

python3 mcchecker.py

Then type:

Mcchecker start

Follow the prompt to enter the Minecraft server IP:

Please insert your minecraft ip
> play.hypixel.net


---

Optional CLI flags

Use Rich UI (colorful tables & panels)


python3 mcchecker.py --rich

Show version and exit


python3 mcchecker.py --version
# Output: Minecraft Server Checker by B-dev — version 1.7 Stable


---

🖼 Example Output

------------
Successfully
------------

Host name : play.hypixel.net
Server name : Hypixel Network [1.8-1.20]
Minecraft server : 172.65.213.132
Operating system : Linux (Termux)
Discord of something : -

Status : online
Player : 65342/200000
Ping : 91 ms

Ports:
  TCP 25565  open   89 ms
  UDP 19132  closed -

With --rich, the output will include colored tables and panels for a nicer display.


---

⚠ Important

Only scan servers you own or have permission to check.

Use responsibly! Unauthorized scanning may violate laws or terms of service.



---

📜 License

MIT License
© 2025 B-dev
---
