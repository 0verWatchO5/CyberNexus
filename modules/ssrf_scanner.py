import requests
import time

class SSRFScanner:
    def __init__(self):
        self.name = "SSRF Scanner"
        self.description = "Scans for Server-Side Request Forgery vulnerabilities"
        
    def scan(self, url, verbose=False, delay=0.5):
        results = []
        test_payloads = [
            "http://127.0.0.1",
            "http://localhost",
            "http://169.254.169.254"  # AWS Metadata IP
        ]

        for payload in test_payloads:
            test_url = f"{url}?url={payload}"
            try:
                response = requests.get(test_url, timeout=10)
                if "root:x" in response.text or "meta-data" in response.text.lower():
                    results.append({
                        'vulnerable': True,
                        'payload': payload,
                        'url': test_url,
                        'evidence': response.text[:200]
                    })
                    if verbose:
                        print(f"[+] SSRF detected with payload: {payload}")
                else:
                    if verbose:
                        print(f"[-] No SSRF detected with: {payload}")
            except requests.RequestException as e:
                if verbose:
                    print(f"[!] Request error with payload {payload}: {e}")
            time.sleep(delay)

        return results
