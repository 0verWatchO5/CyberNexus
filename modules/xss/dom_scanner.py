"""
DOM XSS Scanner Module - Detects DOM-based Cross-Site Scripting vulnerabilities
"""

import requests
from urllib.parse import urljoin, urlparse, parse_qs
import re
import time
import random
from bs4 import BeautifulSoup
from rich.console import Console
from colorama import Fore, Style
import json

console = Console()

class DOMXSSScanner:
    def __init__(self):
        self.name = "DOM XSS Scanner"
        self.description = "Detects DOM-based Cross-Site Scripting vulnerabilities"
        
        # DOM XSS specific payloads
        self.dom_payloads = [
            "#<img src=x onerror=alert('XSS')>",
            "#<script>alert('XSS')</script>",
            "#javascript:alert('XSS')",
            "#'-alert('XSS')-'",
            "#'-alert(document.domain)-'",
            "#<svg/onload=alert('XSS')>",
            "?name=<img src=x onerror=alert('XSS')>",
            "?q=<script>alert('XSS')</script>",
            "?search=<svg/onload=alert('XSS')>",
            "?id=<img src=x onerror=alert('XSS')>",
            "?returnUrl=javascript:alert('XSS')",
            "?returnUrl=data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk7PC9zY3JpcHQ+"
        ]
        
        # DOM sinks that are commonly vulnerable
        self.dom_sinks = [
            "document.URL",
            "document.documentURI",
            "document.URLUnencoded",
            "document.baseURI",
            "location",
            "location.href",
            "location.search",
            "location.hash",
            "location.pathname",
            "document.cookie",
            "document.referrer",
            "window.name",
            "history.pushState",
            "history.replaceState",
            "localStorage",
            "sessionStorage",
            "eval",
            "setTimeout",
            "setInterval",
            "document.write",
            "document.writeln",
            "innerHTML",
            "outerHTML",
            "insertAdjacentHTML",
            "jQuery.html",
            "$"
        ]
        
        # Generate unique identifiers for each scan
        self.scan_id = f"domxss{random.randint(10000, 99999)}"
        
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
            console.print(f"[bold blue]Starting DOM XSS scan on {url}[/bold blue]")
        else:
            print(f"{Fore.BLUE}[*] Starting DOM XSS scan on {url}{Style.RESET_ALL}")
        
        vulnerabilities = []
        
        try:
            # First, analyze the page for potential DOM XSS sinks
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract all JavaScript from the page
            scripts = soup.find_all('script')
            inline_js = [script.string for script in scripts if script.string]
            
            # Extract script sources
            script_srcs = [script.get('src') for script in scripts if script.get('src')]
            
            # Check for DOM sinks in inline JavaScript
            potential_sinks = []
            for js in inline_js:
                if js:
                    for sink in self.dom_sinks:
                        if sink in js:
                            potential_sinks.append(sink)
                            if verbose:
                                console.print(f"[yellow]Potential DOM XSS sink found:[/yellow] {sink}")
                            else:
                                print(f"{Fore.YELLOW}[*] Potential DOM XSS sink found: {sink}{Style.RESET_ALL}")
            
            # Download and check external scripts
            for src in script_srcs:
                script_url = urljoin(url, src)
                try:
                    script_response = requests.get(script_url, headers=self.headers, timeout=10)
                    for sink in self.dom_sinks:
                        if sink in script_response.text:
                            potential_sinks.append(sink)
                            if verbose:
                                console.print(f"[yellow]Potential DOM XSS sink found in external script {src}:[/yellow] {sink}")
                            else:
                                print(f"{Fore.YELLOW}[*] Potential DOM XSS sink found in external script {src}: {sink}{Style.RESET_ALL}")
                except Exception as e:
                    if verbose:
                        console.print(f"[red]Error fetching external script {src}:[/red] {str(e)}")
                    else:
                        print(f"{Fore.RED}[!] Error fetching external script {src}: {str(e)}{Style.RESET_ALL}")
            
            # Look for event handlers in HTML elements
            for tag in soup.find_all():
                for attr in tag.attrs:
                    if attr.startswith('on'):  # Event handler
                        if verbose:
                            console.print(f"[yellow]Event handler found:[/yellow] <{tag.name} {attr}=\"{tag[attr]}\">")
                        else:
                            print(f"{Fore.YELLOW}[*] Event handler found: <{tag.name} {attr}=\"{tag[attr]}\">{Style.RESET_ALL}")
                        potential_sinks.append(f"Event handler: {attr}")
            
            # Test DOM XSS payloads
            for payload in self.dom_payloads:
                test_url = urljoin(url, payload)
                if verbose:
                    console.print(f"[cyan]Testing DOM XSS payload:[/cyan] {payload}")
                else:
                    print(f"{Fore.CYAN}[*] Testing DOM XSS payload: {payload}{Style.RESET_ALL}")
                
                if self._test_dom_xss(test_url, payload, verbose):
                    vulnerabilities.append(f"Potential DOM XSS vulnerability found with payload: {payload}")
                time.sleep(delay)  # Add delay between requests
            
            # If we found potential sinks but no confirmed vulnerabilities, report them
            if potential_sinks and not vulnerabilities:
                sink_str = ", ".join(set(potential_sinks))
                vulnerabilities.append(f"Potential DOM XSS sinks found but no confirmed vulnerabilities: {sink_str}")
                
        except Exception as e:
            error_msg = f"Error during DOM XSS scan: {str(e)}"
            if verbose:
                console.print(f"[bold red]{error_msg}[/bold red]")
            else:
                print(f"{Fore.RED}[!] {error_msg}{Style.RESET_ALL}")
            return [error_msg]
            
        if not vulnerabilities:
            vulnerabilities.append("No DOM XSS vulnerabilities found")
            
        return vulnerabilities
    
    def _test_dom_xss(self, url, payload, verbose=False):
        try:
            # Use a headless browser or specialized DOM XSS detection
            # For this evil, we'll use a simplified approach with regular requests
            response = requests.get(url, headers=self.headers, timeout=10)
            
            # Check if our payload is reflected in a way that might execute
            # This is a simplified check and might have false positives/negatives
            
            # Look for signs that the payload might have been executed
            # For evil, if we see our payload in script tags or event handlers
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check if payload appears in script tags
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and payload in script.string:
                    if verbose:
                        console.print(f"[bold red]DOM XSS payload found in script tag![/bold red]")
                    return True
            
            # Check if payload appears in event handlers
            for tag in soup.find_all():
                for attr, value in tag.attrs.items():
                    if attr.startswith('on') and isinstance(value, str) and payload in value:
                        if verbose:
                            console.print(f"[bold red]DOM XSS payload found in {attr} event handler![/bold red]")
                        return True
            
            # Check for signs of JavaScript execution
            # This is a very simplified check and would need a real browser for accurate testing
            if 'alert' in payload and 'alert' in response.text and payload in response.text:
                if verbose:
                    console.print(f"[bold red]DOM XSS payload potentially executed![/bold red]")
                return True
                
            return False
            
        except Exception as e:
            if verbose:
                console.print(f"[red]Error testing DOM XSS:[/red] {str(e)}")
            return False