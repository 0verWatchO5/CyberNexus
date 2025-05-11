"""
Stored XSS Scanner Module - Attempts to detect Stored Cross-Site Scripting vulnerabilities
"""

import requests
from urllib.parse import urljoin, urlparse, parse_qs
import re
import time
import random
import string
from bs4 import BeautifulSoup
from rich.console import Console
from colorama import Fore, Style

console = Console()

class StoredXSSScanner:
    def __init__(self):
        self.name = "Stored XSS Scanner"
        self.description = "Attempts to detect Stored Cross-Site Scripting vulnerabilities"
        
        # Generate unique identifiers for each scan to detect stored XSS
        self.scan_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        # Stored XSS payloads with unique identifiers
        self.payloads = [
            f"<script>console.log('XSS-{self.scan_id}')</script>",
            f"<img src=x onerror=console.log('XSS-{self.scan_id}')>",
            f"<svg onload=console.log('XSS-{self.scan_id}')>",
            f"<div id='XSS-{self.scan_id}'>XSS Test</div>",
            f"<!--XSS-{self.scan_id}-->",
            f"<script>alert('XSS-{self.scan_id}')</script>",
            f"<img src=x onerror=alert('XSS-{self.scan_id}')>"
        ]
        
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
            console.print(f"[bold blue]Starting Stored XSS scan on {url}[/bold blue]")
            console.print("[yellow]Note: Stored XSS detection requires user interaction and is limited in automated scanning[/yellow]")
        else:
            print(f"{Fore.BLUE}[*] Starting Stored XSS scan on {url}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Note: Stored XSS detection requires user interaction and is limited in automated scanning{Style.RESET_ALL}")
        
        vulnerabilities = []
        
        try:
            # First, identify forms that might store data
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find forms that might store data (e.g., comment forms, registration forms)
            forms = soup.find_all('form')
            potential_storage_forms = []
            
            for i, form in enumerate(forms):
                form_action = form.get('action', '')
                form_method = form.get('method', 'get').lower()
                
                # Forms that use POST are more likely to store data
                if form_method == 'post':
                    form_url = urljoin(url, form_action) if form_action else url
                    
                    # Look for textareas, which often indicate content storage
                    textareas = form.find_all('textarea')
                    
                    # Look for keywords in form or input names that suggest storage
                    storage_keywords = ['comment', 'post', 'message', 'content', 'blog', 'forum', 'reply', 'review', 'feedback']
                    
                    form_text = form.get_text().lower()
                    form_has_storage_keywords = any(keyword in form_text for keyword in storage_keywords)
                    
                    inputs = form.find_all(['input', 'textarea'])
                    input_has_storage_keywords = False
                    
                    for input_field in inputs:
                        input_name = input_field.get('name', '').lower()
                        input_id = input_field.get('id', '').lower()
                        input_placeholder = input_field.get('placeholder', '').lower()
                        
                        if any(keyword in input_name or keyword in input_id or keyword in input_placeholder for keyword in storage_keywords):
                            input_has_storage_keywords = True
                            break
                    
                    if textareas or form_has_storage_keywords or input_has_storage_keywords:
                        potential_storage_forms.append({
                            'form_index': i,
                            'form': form,
                            'form_url': form_url,
                            'form_method': form_method,
                            'inputs': inputs
                        })
            
            if not potential_storage_forms:
                if verbose:
                    console.print("[yellow]No forms that potentially store data were found[/yellow]")
                else:
                    print(f"{Fore.YELLOW}[*] No forms that potentially store data were found{Style.RESET_ALL}")
                return ["No forms that potentially store data were found"]
            
            # Test each potential storage form
            for form_data in potential_storage_forms:
                form_index = form_data['form_index']
                form_url = form_data['form_url']
                inputs = form_data['inputs']
                
                if verbose:
                    console.print(f"[cyan]Testing potential storage form #{form_index+1}[/cyan] at {form_url}")
                else:
                    print(f"{Fore.CYAN}[*] Testing potential storage form #{form_index+1} at {form_url}{Style.RESET_ALL}")
                
                # Try to submit the form with our payloads
                for payload in self.payloads:
                    # Prepare form data
                    form_inputs = {}
                    
                    # Fill required fields with dummy data
                    for input_field in inputs:
                        input_name = input_field.get('name')
                        input_type = input_field.get('type', '')
                        
                        if not input_name:
                            continue
                            
                        # Skip submit buttons, hidden fields, etc.
                        if input_type.lower() in ['submit', 'button', 'image', 'reset', 'file']:
                            continue
                            
                        # Fill text-like inputs with our payload
                        if input_type.lower() in ['text', 'textarea', 'search', 'url', 'email', ''] or input_field.name == 'textarea':
                            form_inputs[input_name] = payload
                        # Fill other inputs with appropriate dummy data
                        elif input_type.lower() == 'checkbox' or input_type.lower() == 'radio':
                            form_inputs[input_name] = 'on'
                        elif input_type.lower() == 'password':
                            form_inputs[input_name] = 'Password123!'
                        elif input_type.lower() == 'email':
                            form_inputs[input_name] = f'test-{self.scan_id}@evil.com'
                        else:
                            form_inputs[input_name] = 'test'
                    
                    if verbose:
                        console.print(f"[dim]Submitting form with payload:[/dim] {payload}")
                    
                    try:
                        # Submit the form
                        response = requests.post(form_url, data=form_inputs, headers=self.headers, timeout=10)
                        
                        # Check if submission was successful
                        if response.status_code < 400:
                            if verbose:
                                console.print(f"[green]Form submission successful (Status: {response.status_code})[/green]")
                            else:
                                print(f"{Fore.GREEN}[+] Form submission successful (Status: {response.status_code}){Style.RESET_ALL}")
                            
                            # Now check if our payload is stored by visiting pages where it might appear
                            # This is a simplified approach - in reality, you'd need to know where to look
                            
                            # First, check the response page itself
                            if self._check_for_stored_payload(response.text, payload):
                                vulnerabilities.append(f"Potential Stored XSS found in form #{form_index+1} with payload: {payload}")
                                break
                            
                            # Then check the original page again
                            time.sleep(delay * 2)  # Wait a bit longer for storage to take effect
                            response = requests.get(url, headers=self.headers, timeout=10)
                            if self._check_for_stored_payload(response.text, payload):
                                vulnerabilities.append(f"Potential Stored XSS found in form #{form_index+1} with payload: {payload}")
                                break
                            
                            # Try to find other pages where content might be displayed
                            # This is very site-specific and hard to generalize
                            links = soup.find_all('a')
                            potential_content_pages = []
                            
                            for link in links:
                                href = link.get('href', '')
                                link_text = link.get_text().lower()
                                
                                # Look for links that might lead to content pages
                                content_keywords = ['comment', 'post', 'message', 'view', 'read', 'article', 'blog', 'forum', 'thread']
                                if any(keyword in link_text or keyword in href.lower() for keyword in content_keywords):
                                    potential_content_pages.append(urljoin(url, href))
                            
                            # Check a limited number of potential content pages
                            for i, page_url in enumerate(potential_content_pages[:3]):  # Limit to 3 pages
                                if verbose:
                                    console.print(f"[dim]Checking potential content page:[/dim] {page_url}")
                                
                                try:
                                    page_response = requests.get(page_url, headers=self.headers, timeout=10)
                                    if self._check_for_stored_payload(page_response.text, payload):
                                        vulnerabilities.append(f"Potential Stored XSS found in form #{form_index+1}, payload detected on page: {page_url}")
                                        break
                                except Exception as e:
                                    if verbose:
                                        console.print(f"[red]Error checking content page {page_url}:[/red] {str(e)}")
                                
                                time.sleep(delay)  # Add delay between requests
                        else:
                            if verbose:
                                console.print(f"[yellow]Form submission failed (Status: {response.status_code})[/yellow]")
                            else:
                                print(f"{Fore.YELLOW}[*] Form submission failed (Status: {response.status_code}){Style.RESET_ALL}")
                    
                    except Exception as e:
                        if verbose:
                            console.print(f"[red]Error submitting form:[/red] {str(e)}")
                        else:
                            print(f"{Fore.RED}[!] Error submitting form: {str(e)}{Style.RESET_ALL}")
                    
                    time.sleep(delay)  # Add delay between requests
            
        except Exception as e:
            error_msg = f"Error during Stored XSS scan: {str(e)}"
            if verbose:
                console.print(f"[bold red]{error_msg}[/bold red]")
            else:
                print(f"{Fore.RED}[!] {error_msg}{Style.RESET_ALL}")
            return [error_msg]
            
        if not vulnerabilities:
            vulnerabilities.append("No Stored XSS vulnerabilities detected (Note: Limited detection capability in automated scanning)")
            
        return vulnerabilities
    
    def _check_for_stored_payload(self, content, payload):
        # Check if our unique payload is in the response
        # This is a simplified check - in reality, you'd need more sophisticated detection
        
        # Extract the unique identifier from the payload
        scan_id_match = re.search(r'XSS-([a-zA-Z0-9]+)', payload)
        if not scan_id_match:
            return False
            
        scan_id = scan_id_match.group(0)  # The full XSS-{id} string
        
        # Check if the unique identifier is in the content
        if scan_id in content:
            # Now check if it's in a context where it might execute
            soup = BeautifulSoup(content, 'html.parser')
            
            # Check if it's in a script tag
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and scan_id in script.string:
                    return True
            
            # Check if it's in an event handler
            for tag in soup.find_all():
                for attr, value in tag.attrs.items():
                    if attr.startswith('on') and isinstance(value, str) and scan_id in value:
                        return True
            
            # Check if our div ID or img tag is present
            if soup.find(id=scan_id) or soup.find('img', attrs={'onerror': lambda v: v and scan_id in v}):
                return True
            
            # It's in the content but not in an executable context
            # This might still be a vulnerability, but less severe
            return True
            
        return False