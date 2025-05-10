import json
from core import scanner
from rich.console import Console

console = Console()

def run_profile(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    for entry in data["targets"]:
        url = entry["url"]
        scans = entry["scan"]
        console.print(f"[cyan][*][/cyan] Profile Scan: {url}")
        if "xss" in scans: scanner.check_reflected_xss(url)
        if "clickjacking" in scans: scanner.check_clickjacking(url)
        if "lfi" in scans: scanner.check_lfi(url)
        if "ssrf" in scans: scanner.check_ssrf(url)
