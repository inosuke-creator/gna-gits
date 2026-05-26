import subprocess
import time
import json
import os
import sys
import requests
from datetime import datetime
from rich.console import Console
from rich.live import Live
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
    "check_interval": 12,
    "auto_rejoin": True,
    "discord_webhook": "",
    "auto_execute_enabled": False,
    "executor_path": ""
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        console.print("[green]✅ Config created![/green]")
        return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def mask_username(username):
    if len(username) <= 4:
        return username
    return username[:2] + "*" * (len(username)-4) + username[-2:]

def set_discord_webhook():
    console.print("\n[yellow]Enter your Discord Webhook URL:[/yellow]")
    webhook = input("> ").strip()
    if webhook.startswith("https://discord.com/api/webhooks"):
        config = load_config()
        config["discord_webhook"] = webhook
        save_config(config)
        console.print("[green]✅ Discord Webhook saved successfully![/green]")
    else:
        console.print("[red]Invalid webhook URL.[/red]")

def edit_game_settings():
    console.print("\n[1] Game ID Only (Public Server)")
    console.print("[2] Private Server")
    choice = input("Choose (1/2): ").strip()

    config = load_config()

    if choice == "1":
        console.print("[yellow]Enter Place ID:[/yellow]")
        config["place_id"] = int(input("> "))
        config["job_id"] = ""
    elif choice == "2":
        console.print("[yellow]Enter Private Server Link:[/yellow]")
        link = input("> ").strip()
        # Basic parsing if it's a roblox.com link
        if "roblox.com" in link and "privateServerLinkCode" in link:
            console.print("[green]Private server link detected.[/green]")
        console.print("[yellow]Enter Job ID (from executor print(game.JobId)):[/yellow]")
        config["job_id"] = input("> ").strip()
        console.print("[yellow]Enter Place ID:[/yellow]")
        config["place_id"] = int(input("> "))
    else:
        console.print("[red]Invalid choice.[/red]")
        return

    save_config(config)
    console.print("[green]✅ Game settings updated![/green]")

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

def send_discord_notification(webhook, message):
    if not webhook:
        return
    try:
        requests.post(webhook, json={"content": message}, timeout=5)
    except:
        pass

# ================== DASHBOARD ==================
def create_dashboard(status, last_rejoin, uptime, config, package):
    table = Table(box=box.ROUNDED, title="🔄 Rejoin Tool - Free Version", title_style="bold cyan")
    table.add_column("Feature", style="bold")
    table.add_column("Status", style="green")

    table.add_row("Auto Rejoin", "[green]ON[/green]" if config.get("auto_rejoin") else "[red]OFF[/red]")
    table.add_row("Current Package", package or "[red]Not Found[/red]")
    table.add_row("Place ID", str(config.get("place_id")))
    table.add_row("Job ID", config.get("job_id")[:12] + "..." if config.get("job_id") else "None")
    table.add_row("Last Rejoin", last_rejoin or "Never")
    table.add_row("Uptime", uptime)
    table.add_row("Discord Webhook", "✅ Set" if config.get("discord_webhook") else "[red]Not Set[/red]")

    footer = "[1] Start Auto Rejoin   [2] Edit Game   [3] Add Discord   [4] Toggle Auto Execute   [q] Quit"
    return Panel(table, border_style="blue", subtitle=footer)

# ================== MAIN ==================
def main():
    console.clear()
    console.print("[bold magenta]=== Rejoin Tool Free Dashboard v6 ===[/bold magenta]\n")
    
    config = load_config()
    start_time = datetime.now()
    last_rejoin = None
    status = "Ready"

    while True:
        uptime = str(datetime.now() - start_time).split('.')[0]
        package = detect_roblox()

        console.clear()
        console.print(create_dashboard(status, last_rejoin, uptime, config, package))

        # Menu Input
        choice = input("\nEnter option: ").strip().lower()

        if choice == "1":
            config["auto_rejoin"] = True
            save_config(config)
            console.print("[green]Auto Rejoin Started![/green]")
            time.sleep(1.5)

        elif choice == "2":
            edit_game_settings()
            time.sleep(1.5)

        elif choice == "3":
            set_discord_webhook()
            time.sleep(1.5)

        elif choice == "4":
            config["auto_execute_enabled"] = not config.get("auto_execute_enabled", False)
            save_config(config)
            console.print(f"Auto Execute: {'[green]Enabled[/green]' if config['auto_execute_enabled'] else '[red]Disabled[/red]'}")
            time.sleep(1.5)

        elif choice == "q":
            console.print("[red]Goodbye![/red]")
            break

        # Auto Rejoin Logic (runs when enabled)
        if config.get("auto_rejoin") and package:
            try:
                recents = subprocess.check_output(["dumpsys", "activity", "recents"], text=True).lower()
                if "roblox" not in recents:
                    status = "Rejoining..."
                    kill_roblox(package)
                    if launch_roblox(package, config["place_id"], config["job_id"]):
                        last_rejoin = datetime.now().strftime("%H:%M:%S")
                        status = "Rejoined Successfully"
                        send_discord_notification(config.get("discord_webhook"), "✅ Roblox Rejoined Successfully!")
            except:
                pass

def kill_roblox(package):
    subprocess.run(["am", "force-stop", package], check=False, stderr=subprocess.DEVNULL)

def launch_roblox(package, place_id, job_id):
    if not job_id:
        deep_link = f"roblox://placeID={place_id}"
    else:
        deep_link = f"roblox://placeID={place_id}&gameInstanceId={job_id}"
    try:
        subprocess.run(["am", "start", "-a", "android.intent.action.VIEW", "-d", deep_link, package], check=True, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Tool stopped.[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
