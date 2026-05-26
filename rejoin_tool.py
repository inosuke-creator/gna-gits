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

console = Console()

CONFIG_FILE = "rejoin_config.json"
SCRIPT_URL = "https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/rejoin_tool.py"

DEFAULT_CONFIG = {
    "place_id": 1234567890,
    "job_id": "YOUR_PRIVATE_SERVER_JOB_ID_HERE",
    "preferred_package": "",
    "check_interval": 15,
    "auto_update": True,
    "check_update_interval": 1800   
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        console.print(f"[green]✅ Config created: {CONFIG_FILE}[/green]")
        console.print("[yellow]Please edit place_id and job_id then restart.[/yellow]")
        sys.exit(0)

def download_script():
    try:
        console.print("[cyan]🔄 Checking for updates...[/cyan]")
        r = requests.get(SCRIPT_URL, timeout=10)
        r.raise_for_status()
        with open(__file__, "w", encoding="utf-8") as f:
            f.write(r.text)
        console.print("[green]✅ Tool Updated! Please restart.[/green]")
        return True
    except:
        console.print("[red]Update check failed.[/red]")
        return False

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
        return None, []
    
    preferred = config.get("preferred_package", "").strip()
    if preferred and preferred in packages:
        return preferred, packages
    return packages[0], packages

def kill_roblox(package):
    try:
        subprocess.run(["am", "force-stop", package], check=True, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def launch_roblox(package, place_id, job_id):
    deep_link = f"roblox://placeID={place_id}&gameInstanceId={job_id}"
    try:
        subprocess.run(["am", "start", "-a", "android.intent.action.VIEW", "-d", deep_link, package],
                       check=True, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def create_dashboard(current_package, all_packages, status, last_rejoin, uptime, config):
    table = Table(box=box.ROUNDED, title="🔄 Rejoin Tool - Auto Reconnect Manager", title_style="bold cyan")
    table.add_column("Item", style="bold")
    table.add_column("Value", style="green")

    table.add_row("Current Package", current_package or "[red]None[/red]")
    table.add_row("Detected Packages", ", ".join(all_packages) if all_packages else "[red]None[/red]")
    table.add_row("Status", status)
    table.add_row("Last Rejoin", last_rejoin or "Never")
    table.add_row("Uptime", uptime)
    table.add_row("Place ID", str(config["place_id"]))
    table.add_row("Check Interval", f"{config['check_interval']}s")

    footer = "Controls: [q] Quit • [r] Manual Rejoin • [u] Update"
    return Panel(table, border_style="blue", subtitle=footer)

def main():
    console.clear()
    console.print("[bold magenta]=== Rejoin Tool v6 (Free Version) ===[/bold magenta]\n")
    
    config = load_config()
    start_time = datetime.now()
    last_rejoin = None
    status = "Starting..."
    last_update_check = time.time()

    with Live(refresh_per_second=2, console=console) as live:
        while True:
            uptime = str(datetime.now() - start_time).split('.')[0]

            if config.get("auto_update") and (time.time() - last_update_check > config.get("check_update_interval")):
                download_script()
                last_update_check = time.time()

            package, all_packages = detect_roblox()

            if not package:
                status = "[red]No Roblox Detected[/red]"
            else:
                try:
                    recents = subprocess.check_output(["dumpsys", "activity", "recents"], text=True).lower()
                    if "roblox" not in recents:
                        status = "[yellow]Rejoining...[/yellow]"
                        live.update(create_dashboard(package, all_packages, status, last_rejoin, uptime, config))
                        
                        kill_roblox(package)
                        if launch_roblox(package, config["place_id"], config["job_id"]):
                            last_rejoin = datetime.now().strftime("%H:%M:%S")
                            status = "[green]✅ Rejoined Successfully[/green]"
                        else:
                            status = "[red]Rejoin Failed[/red]"
                    else:
                        status = "[green]✅ Roblox is Running[/green]"
                except:
                    status = "[yellow]Monitoring...[/yellow]"
                    launch_roblox(package, config["place_id"], config["job_id"])
                    last_rejoin = datetime.now().strftime("%H:%M:%S")

            live.update(create_dashboard(package, all_packages, status, last_rejoin, uptime, config))
            time.sleep(config["check_interval"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Tool Stopped.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
