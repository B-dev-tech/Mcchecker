#!/usr/bin/env python3
"""
Minecraft Server Checker 🟩
By B-dev
Version: 1.7 Stable

Usage:
    python3 mcchecker.py [--rich] [--version]
"""

import socket
import time
import platform
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from mcstatus import JavaServer
except ImportError:
    print("❌ Missing dependency: mcstatus\nInstall with: pip install mcstatus")
    sys.exit(1)

# Optional Rich UI
USE_RICH = "--rich" in sys.argv
SHOW_VERSION = "--version" in sys.argv

VERSION = "1.7 Stable"

if SHOW_VERSION:
    print(f"Minecraft Server Checker by B-dev — version {VERSION}")
    sys.exit(0)

if USE_RICH:
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
    except ImportError:
        print("❌ Missing dependency for rich mode. Install with: pip install rich")
        sys.exit(1)
    console = Console()

# Settings
TCP_PORTS = [25565]
UDP_PORTS = [19132]
OTHER_PORTS = [11, 21]
TCP_TIMEOUT = 3
UDP_TIMEOUT = 2
MAX_WORKERS = 40


def detect_os():
    system = platform.system()
    release = platform.release()
    if "ANDROID_ROOT" in os.environ or "com.termux" in os.getcwd():
        return "Linux (Termux)"
    return f"{system} {release}"


def tcp_check(host, port, timeout=TCP_TIMEOUT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    start = time.time()
    try:
        s.connect((host, port))
        elapsed = int((time.time() - start) * 1000)
        s.close()
        return True, elapsed, ""
    except Exception as e:
        return False, None, str(e)
    finally:
        try:
            s.close()
        except:
            pass


def udp_check(host, port, timeout=UDP_TIMEOUT):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(timeout)
    try:
        s.sendto(b"\x00", (host, port))
        try:
            data, addr = s.recvfrom(1024)
            return True, 0, ""
        except socket.timeout:
            return False, None, "timeout"
    except Exception as e:
        return False, None, str(e)
    finally:
        s.close()


def query_mcstatus(host, port=25565):
    try:
        server = JavaServer.lookup(f"{host}:{port}")
        status = server.status()
        motd = str(status.description)
        return {
            "name": motd,
            "players_online": status.players.online,
            "players_max": status.players.max,
            "version": status.version.name,
            "ping_ms": int(status.latency)
        }
    except Exception:
        return None


def print_banner():
    banner = f"""
============================================================
               Minecraft server checker
                   By B-dev ({VERSION})
============================================================
"""
    print(banner)


def scan_and_report(target):
    host = target.split(":")[0]
    port = 25565
    if ":" in target:
        try:
            port = int(target.split(":")[1])
        except ValueError:
            port = 25565

    try:
        ipaddr = socket.gethostbyname(host)
    except Exception:
        ipaddr = host

    mc_info = query_mcstatus(host, port)

    if not USE_RICH:
        print("------------")
        print("Successfully")
        print("------------\n")
        print(f"Host name : {host}")
        print(f"Server name : {mc_info['name'] if mc_info else '-'}")
        print(f"Minecraft server : {ipaddr}")
        print(f"Operating system : {detect_os()}")
        print("Discord of something : -\n")
        print(f"Status : {'online' if mc_info else 'unknown'}")
        if mc_info:
            print(f"Player : {mc_info['players_online']}/{mc_info['players_max']}")
            print(f"Ping : {mc_info['ping_ms']} ms\n")
        else:
            print("Player : -")
            print("Ping : -\n")
    else:
        panel = Panel.fit(
            f"[bold green]Successfully[/bold green]\n\n"
            f"[cyan]Host name:[/cyan] {host}\n"
            f"[cyan]Server name:[/cyan] {mc_info['name'] if mc_info else '-'}\n"
            f"[cyan]Minecraft server:[/cyan] {ipaddr}\n"
            f"[cyan]Operating system:[/cyan] {detect_os()}\n"
            f"[cyan]Discord of something:[/cyan] -\n",
            title="Minecraft Server Info",
            border_style="green"
        )
        console.print(panel)

    ports_to_check = TCP_PORTS + UDP_PORTS + OTHER_PORTS
    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as exe:
        futures = {}
        for p in TCP_PORTS + OTHER_PORTS:
            futures[exe.submit(tcp_check, host, p)] = ("TCP", p)
        for p in UDP_PORTS:
            futures[exe.submit(udp_check, host, p)] = ("UDP", p)

        for fut in as_completed(futures):
            proto, p = futures[fut]
            ok, rtt, err = fut.result()
            results.append((proto, p, ok, rtt, err))

    if USE_RICH:
        table = Table(title="Port Scan Results", show_header=True, header_style="bold magenta")
        table.add_column("Protocol", width=6)
        table.add_column("Port", width=8)
        table.add_column("Status", width=15)
        table.add_column("RTT (ms)", width=10)

        for proto, p, ok, rtt, err in results:
            state = "[green]open[/green]" if ok else "[red]closed[/red]"
            table.add_row(proto, str(p), state, str(rtt or "-"))
        console.print(table)
    else:
        print("------------------------------------------------------------")
        print("Ports")
        print("------------------------------------------------------------")
        for proto, p, ok, rtt, err in results:
            print(f"{proto:<5} {p:<6} {'open' if ok else 'closed'}  {rtt or '-'} ms")

    print("\n------------------------------------------------------------")
    print("Scan completed.")
    print("------------------------------------------------------------\n")


def main():
    print("Type 'Mcchecker start' to begin (or 'exit' to quit).")
    while True:
        cmd = input("> ").strip()
        if cmd.lower() in ("exit", "quit"):
            print("Bye.")
            break
        if cmd.lower() == "mcchecker start":
            print_banner()
            target = input("Please insert your minecraft ip\n> ").strip()
            if target:
                print("\n[!] Make sure you have permission to scan this target.\n")
                scan_and_report(target)
            else:
                print("No target provided.")
        else:
            print("Unknown command. Try 'Mcchecker start' or 'exit'.")


if __name__ == "__main__":
    main()
