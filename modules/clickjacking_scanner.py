"""
Clickjacking Scanner Module - Checks for X-Frame-Options and CSP frame-ancestors
"""

import requests
from urllib.parse import urlparse
from rich.console import Console
from colorama import Fore, Style
import time

console = Console()

class ClickjackingScanner:
    def __init__(self):
        self.name = "Clickjacking Scanner"
        self.description = "Checks for X-Frame-Options and CSP frame-ancestors headers"
        self.headers = {
            'User-Agent': 'CyberNexus/1.0 Security Scanner',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1'
        }
        
    def scan(self, url, verbose=False, delay=0.5):
        if verbose:
            console.print(f"[bold blue]Starting Clickjacking scan on {url}[/bold blue]")
        else:
            print(f"{Fore.BLUE}[*] Starting Clickjacking scan on {url}{Style.RESET_ALL}")
        
        results = {
            'vulnerable': False,
            'x_frame_options': None,
            'csp_frame_ancestors': None,
            'details': []
        }
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            # Check X-Frame-Options header
            x_frame_options = response.headers.get('X-Frame-Options', '').upper()
            results['x_frame_options'] = x_frame_options
            
            if verbose:
                if x_frame_options:
                    console.print(f"[green]X-Frame-Options header found:[/green] {x_frame_options}")
                else:
                    console.print("[yellow]X-Frame-Options header not found[/yellow]")
            
            # Check Content-Security-Policy header for frame-ancestors directive
            csp = response.headers.get('Content-Security-Policy', '')
            frame_ancestors = None
            
            if csp:
                for directive in csp.split(';'):
                    directive = directive.strip()
                    if directive.startswith('frame-ancestors'):
                        frame_ancestors = directive[len('frame-ancestors'):].strip()
                        break
            
            results['csp_frame_ancestors'] = frame_ancestors
            
            if verbose:
                if frame_ancestors:
                    console.print(f"[green]CSP frame-ancestors directive found:[/green] {frame_ancestors}")
                else:
                    console.print("[yellow]CSP frame-ancestors directive not found[/yellow]")

            # Determine vulnerability
            if not x_frame_options and not frame_ancestors:
                results['vulnerable'] = True
                results['details'].append("No X-Frame-Options or CSP frame-ancestors header found.")
                if verbose:
                    console.print(f"[bold red]Potential Clickjacking vulnerability detected![/bold red]")
                else:
                    print(f"{Fore.RED}[!] Potential Clickjacking vulnerability detected!{Style.RESET_ALL}")
            else:
                results['details'].append("At least one protective header is present.")
                if verbose:
                    console.print(f"[bold green]No Clickjacking vulnerability detected.[/bold green]")
                else:
                    print(f"{Fore.GREEN}[+] No Clickjacking vulnerability detected.{Style.RESET_ALL}")

        except requests.exceptions.RequestException as e:
            results['details'].append(f"Error fetching URL: {str(e)}")
            if verbose:
                console.print(f"[red]Error fetching URL:[/red] {e}")
            else:
                print(f"{Fore.RED}[!] Error fetching URL: {e}{Style.RESET_ALL}")
        
        time.sleep(delay)
        return results
