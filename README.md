# CyberNexus

A modular CLI-based web security scanning tool with enhanced XSS detection capabilities and a beautiful command-line interface.

![CyberNexus Banner](https://mayureshchaubal.netlify.app/banner.png)

---

## 🚀 Features

-   ✅ Advanced XSS Detection
    -   Reflected XSS Detection with context-aware payloads
    -   DOM-based XSS Detection with source-sink analysis
    -   Stored XSS Detection with unique payload tracking
-   ✅ Clickjacking Header Scanner
-   ✅ Local File Inclusion (LFI) Tester
-   ✅ Server-Side Request Forgery (SSRF) Tester
-   ✅ Profile-based batch scans
-   ✅ GitHub-based plugin auto-updater
-   ✅ Beautiful CLI interface with rich and colorama
-   ✅ Interactive scanning mode
-   ✅ Comprehensive HTML, JSON, and text reports

---

## 📦 Installation

Clone the repo and then follow the steps for your OS.
> Note that this tool was made with python3. Make sure python is installed on your system before following the below steps. 

### Windows (PowerShell)

```bash
git clone https://github.com/0verWatchO5/CyberNexus

cd CyberNexus

#Create a python virtual environment in case you do not wish to install the python modules globally.
python -m venv cynx

#Virtual Environments have a different activation command from Linux and Mac. Run this in powershell
.\cynx\Scripts\Activate

#If you wish to install the modules globally you can skip the above two steps and run this command
python -m pip install -r requirements.txt
```

### Linux (Terminal/Bash)

```bash
git clone https://github.com/0verWatchO5/CyberNexus

cd CyberNexus

#Create a python virtual environment, Linux does not let you install the python modules globally or outside a virtual environment
python3 -m venv cynx

#Activate the Virtual environment
source cynx/bin/activate

#Install all the required python modules with a single command
pip install -r requirements.txt
```

### MacOS (Terminal)

```bash
git clone https://github.com/0verWatchO5/CyberNexus

cd CyberNexus

#Create a python virtual environment (Recommended)
python3 -m venv cynx

#Activate the Virtual environment
source cynx/bin/activate

#Install all the required python modules with a single command
pip install -r requirements.txt
```

---

## 🧪 Usage

```bash
# Run a specific scan type on a URL 
python3 cybernexus.py scan -u https://evil.com -t xss-reflected

# Run all XSS scan types on a URL 
python3 cybernexus.py scan -u https://evil.com -t xss-all

# Run all scan types on a URL 
python3 cybernexus.py scan -u https://evil.com -a

# Save scan results to a file 
python3 cybernexus.py scan -u https://evil.com -a -o results.json

# Generate an HTML report 
python3 cybernexus.py scan -u https://evil.com -a -o results.html -f html

# Enable verbose output 
python3 cybernexus.py scan -u https://evil.com -t xss-reflected -v
```

## Interactive Mode

```bash
# Run in interactive mode for guided scanning 
python3 cybernexus.py interactive
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
class MyCustomScanner:    def __init__(self):        
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

1.  Fork the repo
    
2.  Add your new plugin or feature
    
3.  Submit a PR 🚀
    

#### Thank you!