import subprocess
import time
import json
import os
import sys
import requests
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import threading

console = Console()

# ================== CONFIG ==================
CONFIG_FILE = "rejoin_config.json"
SCRIPT_URL = "https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/rejoin_tool.py"

DEFAULT_CONFIG = {
    "place_id": 1234567890,
    "job_id": "",
    "preferred_package": "",
    "check_interval": 10,
    "auto_rejoin": False,        # Forced OFF by default
    "discord_webhook": "",
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def get_all_roblox_packages():
    try:
        result = subprocess.check_output(["pm", "list", "packages"], text=True)
        packages = [line.replace("package:", "").strip() for line in result.splitlines() if line.strip()]
        return [pkg for pkg in packages if pkg.startswith("com.roblox.")]
    except:
        return []

def detect_roblox():
    config = load_config()
    packages = get_all_roblox_packages()
    if not packages:
        return None
    preferred = config.get("preferred_package")
    if preferred and preferred in packages:
        return preferred
    return packages[0]

def kill_roblox(package):
    subprocess.run(["am", "force-stop", package], check=False, stderr=subprocess.DEVNULL)

def launch_roblox(package, place_id, job_id):
    if not job_id or job_id.lower() == "none":
        deep_link = f"roblox://placeID={place_id}"
    else:
        deep_link = f"roblox://placeID={place_id}&gameInstanceId={job_id}"
    try:
        subprocess.run(["am", "start", "-a", "android.intent.action.VIEW", "-d", deep_link, package],
                       check=True, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def create_dashboard(status, last_rejoin, uptime, config, package):
    console.clear()
    
    table = Table(box=box.SIMPLE_HEAVY, title="🔄 Rejoin Tool - Free Version", title_style="bold cyan", expand=True)
    table.add_column("Feature", style="bold", width=20)
    table.add_column("Status", style="green")

    table.add_row("Auto Rejoin", "[green]ON[/green]" if config.get("auto_rejoin") else "[red]OFF[/red]")
    table.add_row("Current Package", package or "[red]Not Detected[/red]")
    table.add_row("Place ID", str(config.get("place_id", "Not Set")))
    table.add_row("Job ID", (config.get("job_id")[:20] + "...") if config.get("job_id") else "None")
    table.add_row("Last Rejoin", last_rejoin or "Never")
    table.add_row("Uptime", uptime)
    table.add_row("Discord Webhook", "[green]Set[/green]" if config.get("discord_webhook") else "[red]Not Set[/red]")

    console.print(Panel(table, border_style="blue"))
    
    footer = "[1] Start Auto Rejoin    [2] Edit Game    [3] Add Discord Webhook    [4] Toggle Auto Execute    [q] Quit"
    console.print(footer, style="bold yellow")

# Background Auto Rejoin Thread
def auto_rejoin_thread(config, stop_event):
    last_rejoin = None
    while not stop_event.is_set():
        if not config.get("auto_rejoin"):
            time.sleep(2)
            continue
            
        package = detect_roblox()
        if package:
            try:
                recents = subprocess.check_output(["dumpsys", "activity", "recents"], text=True).lower()
                if "roblox" not in recents:
                    kill_roblox(package)
                    if launch_roblox(package, config["place_id"], config["job_id"]):
                        last_rejoin = datetime.now().strftime("%H:%M:%S")
            except:
                pass
        time.sleep(config.get("check_interval", 10))

# ================== MAIN ==================
def main():
    console.clear()
    console.print("[bold magenta]=== Rejoin Tool - Free Version ===[/bold magenta]\n")
    
    config = load_config()
    start_time = datetime.now()
    stop_event = threading.Event()
    
    # Start background thread
    rejoin_thread = threading.Thread(target=auto_rejoin_thread, args=(config, stop_event), daemon=True)
    rejoin_thread.start()

    while True:
        uptime = str(datetime.now() - start_time).split('.')[0]
        package = detect_roblox()

        create_dashboard("Running", None, uptime, config, package)

        choice = input("\nEnter option: ").strip().lower()

        if choice == "1":
            config["auto_rejoin"] = True
            save_config(config)
            console.print("[green]Auto Rejoin Enabled![/green]")
            time.sleep(1.2)

        elif choice == "2":
            console.clear()
            console.print("[yellow]=== Edit Game Settings ===[/yellow]\n")
            console.print("[1] Game ID Only\n[2] Private Server")
            ch = input("\nChoose (1/2): ").strip()
            
            if ch == "1":
                try:
                    config["place_id"] = int(input("Enter Place ID: ") or config["place_id"])
                    config["job_id"] = ""
                except:
                    pass
            elif ch == "2":
                try:
                    config["place_id"] = int(input("Enter Place ID: ") or config["place_id"])
                    config["job_id"] = input("Enter Job ID: ").strip()
                except:
                    pass
            
            save_config(config)
            console.print("[green]Game settings saved![/green]")
            time.sleep(1.5)

        elif choice == "3":
            console.clear()
            console.print("[yellow]Enter Discord Webhook URL:[/yellow]")
            webhook = input("> ").strip()
            if webhook:
                config["discord_webhook"] = webhook
                save_config(config)
                console.print("[green]Webhook Saved![/green]")
            time.sleep(1.5)

        elif choice == "4":
            console.print("[yellow]Auto Execute feature coming soon...[/yellow]")
            time.sleep(1.5)

        elif choice == "q":
            stop_event.set()
            console.clear()
            console.print("[red]Tool Stopped.[/red]")
            break

        time.sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.clear()
        console.print("[red]Tool Stopped.[/red]")
    except Exception as e:
        console.clear()
        console.print(f"[red]Error: {e}[/red]")
