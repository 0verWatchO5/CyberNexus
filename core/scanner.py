import requests
from urllib.parse import urlencode
from rich.console import Console

console = Console()

def check_clickjacking(url):
    try:
        res = requests.get(url, timeout=5)
        xfo = res.headers.get("X-Frame-Options")
        csp = res.headers.get("Content-Security-Policy")
        if not xfo and not csp:
            console.print(f"[red][!][/red] Potential Clickjacking: No XFO/CSP headers.")
        else:
            console.print(f"[green][+][/green] Clickjacking protection present.")
    except Exception as e:
        console.print(f"[red][x][/red] Error: {e}")

def check_reflected_xss(url):
    payload = "<script>alert(1)</script>"
    test_url = f"{url}?q={payload}"
    try:
        res = requests.get(test_url, timeout=5)
        if payload in res.text:
            console.print(f"[red][!][/red] Reflected XSS found: {test_url}")
        else:
            console.print(f"[green][+][/green] No XSS at: {test_url}")
    except Exception as e:
        console.print(f"[red][x][/red] Error: {e}")

def check_lfi(url):
    console.print("[cyan][*][/cyan] Testing LFI...")
    for p in ["../../../../etc/passwd", "../../../../windows/win.ini"]:
        try:
            res = requests.get(f"{url}?file={p}", timeout=5)
            if "root:x" in res.text or "[extensions]" in res.text:
                console.print(f"[red][!][/red] LFI at: {url}?file={p}")
                return
        except: pass
    console.print("[green][+][/green] No LFI detected.")

def check_ssrf(url):
    console.print("[cyan][*][/cyan] Testing SSRF...")
    target = "http://169.254.169.254"
    for p in ["url", "uri", "path"]:
        try:
            r = requests.get(f"{url}?{p}={target}", timeout=5)
            if "meta-data" in r.text.lower():
                console.print(f"[red][!][/red] SSRF at: {url}?{p}={target}")
                return
        except: pass
    console.print("[green][+][/green] No SSRF found.")

def run(args):
    if args.url:
        console.print(f"[cyan][*][/cyan] Scanning {args.url}")
        check_clickjacking(args.url)
        check_reflected_xss(args.url)
        check_lfi(args.url)
        check_ssrf(args.url)
