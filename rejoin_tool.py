import subprocess
import time
import json
import os
import sys
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

# ================== CONFIG ==================
CONFIG_FILE = "rejoin_config.json"

DEFAULT_CONFIG = {
    "place_id": 89469502395769,   # Your game
    "job_id": "",
    "check_interval": 8,
    "auto_rejoin": False,
    "discord_webhook": "",
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            config["auto_rejoin"] = False
            return config
    else:
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def get_roblox_package():
    try:
        result = subprocess.check_output(["pm", "list", "packages"], text=True)
        packages = [line.replace("package:", "").strip() for line in result.splitlines() if line.strip()]
        roblox_pkgs = [pkg for pkg in packages if pkg.startswith("com.roblox.")]
        return roblox_pkgs[0] if roblox_pkgs else None
    except:
        return None

def kill_roblox(package):
    subprocess.run(["am", "force-stop", package], check=False, stderr=subprocess.DEVNULL)
    time.sleep(2.5)

def launch_roblox(package, place_id, job_id):
    if not job_id:
        deep_link = f"roblox://placeID={place_id}"
    else:
        deep_link = f"roblox://placeID={place_id}&gameInstanceId={job_id}"
    
    console.print(f"[cyan]→ Launching: {deep_link}[/cyan]")
    
    try:
        # Stronger launch command
        subprocess.run([
            "am", "start",
            "-a", "android.intent.action.VIEW",
            "-d", deep_link,
            "-f", "0x14000000",   # New Task + Clear Top
            package
        ], check=True, stderr=subprocess.DEVNULL)
        
        console.print("[green]✅ Roblox launch command sent![/green]")
        return True
    except Exception as e:
        console.print(f"[red]Launch failed: {e}[/red]")
        return False

def create_dashboard(config, package, last_rejoin, uptime):
    console.clear()
    
    table = Table(box=box.SIMPLE_HEAVY, title="🔄 Rejoin Tool - Free Version", title_style="bold cyan", expand=True)
    table.add_column("Feature", style="bold", width=22)
    table.add_column("Status", style="green")

    table.add_row("Auto Rejoin", "[green]ON[/green]" if config.get("auto_rejoin") else "[red]OFF[/red]")
    table.add_row("Current Package", package or "[red]Not Detected[/red]")
    table.add_row("Place ID", str(config.get("place_id")))
    table.add_row("Job ID", config.get("job_id")[:20] + "..." if config.get("job_id") else "None")
    table.add_row("Last Rejoin", last_rejoin or "Never")
    table.add_row("Uptime", uptime)

    console.print(Panel(table, border_style="blue"))
    console.print("\n[1] Toggle Auto Rejoin   [2] Edit Game   [3] Add Discord   [q] Quit", style="bold yellow")

# ================== MAIN ==================
def main():
    console.clear()
    console.print("[bold magenta]=== Rejoin Tool - Free Version ===[/bold magenta]\n")
    
    config = load_config()
    start_time = datetime.now()
    last_rejoin = None

    while True:
        uptime = str(datetime.now() - start_time).split('.')[0]
        package = get_roblox_package()

        create_dashboard(config, package, last_rejoin, uptime)

        if config.get("auto_rejoin") and package:
            try:
                recents = subprocess.check_output(["dumpsys", "activity", "recents"], text=True).lower()
                if "roblox" not in recents:
                    console.print("[yellow]🔄 Roblox closed → Rejoining now...[/yellow]")
                    kill_roblox(package)
                    if launch_roblox(package, config["place_id"], config["job_id"]):
                        last_rejoin = datetime.now().strftime("%H:%M:%S")
            except:
                pass

        choice = input("\nEnter option: ").strip().lower()

        if choice == "1":
            config["auto_rejoin"] = not config.get("auto_rejoin")
            save_config(config)
            console.print(f"[green]Auto Rejoin is now {'ON' if config['auto_rejoin'] else 'OFF'}[/green]")
            time.sleep(1)

        elif choice == "2":
            console.clear()
            console.print("[yellow]=== Edit Game Settings ===[/yellow]\n")
            console.print("1. Game ID Only\n2. Private Server")
            ch = input("Choose (1/2): ").strip()
            if ch == "1":
                config["place_id"] = int(input("Enter Place ID: ") or config["place_id"])
                config["job_id"] = ""
            elif ch == "2":
                config["place_id"] = int(input("Enter Place ID: ") or config["place_id"])
                config["job_id"] = input("Enter Job ID: ").strip()
            save_config(config)
            console.print("[green]✅ Saved![/green]")
            time.sleep(1.5)

        elif choice == "3":
            console.clear()
            console.print("[yellow]Enter Discord Webhook URL:[/yellow]")
            config["discord_webhook"] = input("> ").strip()
            save_config(config)
            console.print("[green]✅ Saved![/green]")
            time.sleep(1.5)

        elif choice == "q":
            console.clear()
            console.print("[red]Tool Stopped.[/red]")
            break

        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.clear()
        console.print("[red]Tool Stopped.[/red]")
