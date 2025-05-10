import os
import requests
from rich.console import Console

console = Console()

GITHUB_REPO = "https://raw.githubusercontent.com/youruser/cyber-nexus-plugins/main/plugins/"
PLUGIN_DIR = os.path.join(os.path.dirname(__file__), "..", "plugins")

def list_remote_plugins():
    try:
        r = requests.get(GITHUB_REPO + "index.txt")
        if r.status_code == 200:
            return r.text.strip().splitlines()
    except Exception as e:
        console.print(f"[red][x][/red] Failed to fetch plugin index: {e}")
    return []

def download_plugin(plugin_name):
    url = GITHUB_REPO + plugin_name
    path = os.path.join(PLUGIN_DIR, plugin_name)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            with open(path, "w") as f:
                f.write(r.text)
            console.print(f"[green][+][/green] Downloaded: {plugin_name}")
    except Exception as e:
        console.print(f"[red][x][/red] Error: {e}")

def update_all_plugins():
    plugins = list_remote_plugins()
    for plugin in plugins:
        download_plugin(plugin)
