import subprocess
import time
import json
import os
import sys
from datetime import datetime
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

CONFIG_FILE = "rejoin_config.json"

DEFAULT_CONFIG = {
    "place_id": 1234567890,
    "job_id": "YOUR_PRIVATE_SERVER_JOB_ID_HERE",
    "preferred_package": "",
    "check_interval": 15,
    "auto_download": False,
    "download_url": "",
    "download_path": "/sdcard/Download/roblox_update.apk"
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        console.print(f"[green]✅ Created config file: {CONFIG_FILE}[/green]")
        console.print("[yellow]Please edit place_id and job_id, then restart the tool.[/yellow]")
        sys.exit(0)

def get_all_roblox_packages():
    try:
        result = subprocess.check_output(["pm", "list", "packages"], text=True)
        packages = [line.replace("package:", "").strip() for line in result.splitlines() if line.strip()]
        return [pkg for pkg in packages if pkg.startswith("com.roblox.")]
    except:
        return []

def detect_roblox():
    config = load_config()
    roblox_packages = get_all_roblox_packages()
    
    if not roblox_packages:
        return None, []
    
    preferred = config.get("preferred_package", "").strip()
    if preferred and preferred in roblox_packages:
        return preferred, roblox_packages
    
    return roblox_packages[0], roblox_packages

def kill_roblox(package):
    try:
        subprocess.run(["am", "force-stop", package], check=True, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def launch_roblox(package, place_id, job_id):
    deep_link = f"roblox://placeID={place_id}&gameInstanceId={job_id}"
    try:
        subprocess.run([
            "am", "start",
            "-a", "android.intent.action.VIEW",
            "-d", deep_link,
            package
        ], check=True, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def create_dashboard(current_package, all_packages, status, last_rejoin, uptime):
    table = Table(box=box.ROUNDED, title="Roblox Auto Rejoin Tool", title_style="bold cyan")
    table.add_column("Status", style="bold")
    table.add_column("Value", style="green")

    table.add_row("Current Package", current_package or "None")
    table.add_row("All Detected", ", ".join(all_packages) if all_packages else "None")
    table.add_row("Rejoin Status", status)
    table.add_row("Last Rejoin", last_rejoin or "Never")
    table.add_row("Uptime", uptime)
    table.add_row("Place ID", str(load_config()["place_id"]))
    
    return Panel(table, border_style="blue")

def main():
    console.clear()
    console.print("[bold magenta]=== Roblox Auto Rejoin Tool with Dashboard ===[/bold magenta]\n")
    
    config = load_config()
    start_time = datetime.now()
    last_rejoin = None
    status = "Starting..."

    with Live(refresh_per_second=2, console=console) as live:
        while True:
            current_time = datetime.now()
            uptime = str(current_time - start_time).split('.')[0]
            
            package, all_packages = detect_roblox()
            
            if not package:
                status = "[red]No Roblox package detected[/red]"
                live.update(create_dashboard(None, [], status, last_rejoin, uptime))
                time.sleep(config["check_interval"])
                continue

            try:
                recents = subprocess.check_output(["dumpsys", "activity", "recents"], text=True).lower()
                if "roblox" not in recents:
                    status = "[yellow]Rejoining...[/yellow]"
                    live.update(create_dashboard(package, all_packages, status, last_rejoin, uptime))
                    
                    kill_roblox(package)
                    success = launch_roblox(package, config["place_id"], config["job_id"])
                    
                    if success:
                        last_rejoin = datetime.now().strftime("%H:%M:%S")
                        status = "[green]Rejoined successfully[/green]"
                    else:
                        status = "[red]Rejoin failed[/red]"
                else:
                    status = "[green]Roblox is running[/green]"
            except:
                status = "[yellow]Checking...[/yellow]"
                launch_roblox(package, config["place_id"], config["job_id"])
                last_rejoin = datetime.now().strftime("%H:%M:%S")

            live.update(create_dashboard(package, all_packages, status, last_rejoin, uptime))
            time.sleep(config["check_interval"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Tool stopped by user.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
