# CyberNexus

A modular CLI-based web security scanning tool with enhanced XSS detection capabilities and a beautiful command-line interface.

![CyberNexus Banner](https://mayureshchaubal.netlify.app/banner.png)

---

## 🚀 Features

- ✅ Advanced XSS Detection
  - Reflected XSS Detection with context-aware payloads
  - DOM-based XSS Detection with source-sink analysis
  - Stored XSS Detection with unique payload tracking
- ✅ Clickjacking Header Scanner
- ✅ Local File Inclusion (LFI) Tester
- ✅ Server-Side Request Forgery (SSRF) Tester
- ✅ Profile-based batch scans
- ✅ GitHub-based plugin auto-updater
- ✅ Beautiful CLI interface with rich and colorama
- ✅ Interactive scanning mode
- ✅ Comprehensive HTML, JSON, and text reports

---

## 📦 Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/0verWatchO5/CyberNexus
cd CyberNexus
python3 -m venv NEX
pip3 install -r requirements.txt
```

---

## 🧪 Usage
```bash
# Run a specific scan type on a URL
python cybernexus.py scan -u https://evil.com -t xss-reflected

# Run all XSS scan types on a URL
python cybernexus.py scan -u https://evil.com -t xss-all

# Run all scan types on a URL
python cybernexus.py scan -u https://evil.com -a

# Save scan results to a file
python cybernexus.py scan -u https://evil.com -a -o results.json

# Generate an HTML report
python cybernexus.py scan -u https://evil.com -a -o results.html -f html

# Enable verbose output
python cybernexus.py scan -u https://evil.com -t xss-reflected -v
```
## Interactive Mode
```bash
# Run in interactive mode for guided scanning
python cybernexus.py interactive
```

---

## Using Profiles
```bash
# Create a scan profile
python cybernexus.py profile create -n full_scan -t xss-all clickjacking lfi ssrf

# List available profiles
python cybernexus.py profile list

# Run a scan profile on a URL
python cybernexus.py profile run -n full_scan -u https://evil.com
```

---

## Managing Plugins

```bash
# List installed plugins
python cybernexus.py plugin list

# Update all plugins
python cybernexus.py plugin update

# Add a custom plugin
python cybernexus.py plugin add -n my_plugin -r https://github.com/username/my-plugin
```

---

## Want to create and submit your own plugin?
Create a new Python file in your plugin repository with this structure:

```bash
class MyCustomScanner:
    def __init__(self):
        self.name = "My Custom Scanner"
        self.description = "Description of what your scanner does"
        
    def scan(self, url, verbose=False, delay=0.5):
        # Your scanning logic here
        results = []
        # ... perform scanning ...
        return results
```

---

## 🤝 Contributing
Pull requests are welcome! Please follow these steps:

1. Fork the repo

2. Add your new plugin or feature

3. Submit a PR 🚀

#### Thank you!

