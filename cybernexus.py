#!/usr/bin/env python3
"""
CyberNexus - An advanced modular web security scanning tool
"""

import argparse
import sys
import os
import json
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.syntax import Syntax
from rich.text import Text
from rich.tree import Tree
from rich.prompt import Prompt, Confirm
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# Import scanner modules
from modules.xss.reflected_scanner import ReflectedXSSScanner
from modules.xss.dom_scanner import DOMXSSScanner
from modules.xss.stored_scanner import StoredXSSScanner
from modules.clickjacking_scanner import ClickjackingScanner
from modules.lfi_scanner import LFIScanner
from modules.ssrf_scanner import SSRFScanner
from utils.profile_manager import ProfileManager
from utils.plugin_updater import PluginUpdater
from utils.report_generator import ReportGenerator

# Create console for rich output
console = Console()

class CyberNexus:
    def __init__(self):
        self.scanners = {
            'xss-reflected': ReflectedXSSScanner(),
            'xss-dom': DOMXSSScanner(),
            'xss-stored': StoredXSSScanner(),
            'xss-all': None,  # Special case to run all XSS scanners
            'clickjacking': ClickjackingScanner(),
            'lfi': LFIScanner(),
            'ssrf': SSRFScanner()
        }
        self.profile_manager = ProfileManager()
        self.plugin_updater = PluginUpdater()
        self.report_generator = ReportGenerator()
        
    def display_banner(self):
        banner = r"""
  _____      _               _   _                     
 / ____|    | |             | \ | |                    
| |    _   _| |__   ___ _ __|  \| | _____  ___   _ ___ 
| |   | | | | '_ \ / _ \ '__| . ` |/ _ \ \/ / | | / __|
| |___| |_| | |_) |  __/ |  | |\  |  __/>  <| |_| \__ \
 \_____\__, |_.__/ \___|_|  |_| \_|\___/_/\_\\__,_|___/
        __/ |                                          
       |___/                                           
        """
        
        console.print(Panel(Text(banner, style="bold blue"), 
                           title="[bold cyan]CyberNexus Security Scanner[/bold cyan]", 
                           subtitle="[italic]Advanced Web Security Testing Tool[/italic]",
                           border_style="green"))
        
        console.print("\n[bold yellow]🔒 Developed for security professionals and penetration testers[/bold yellow]")
        console.print("[dim]Run with -h for help and available commands[/dim]\n")
        
    def setup_argparse(self):
        parser = argparse.ArgumentParser(
            description='CyberNexus - Advanced Web Security Scanner',
            formatter_class=argparse.RawTextHelpFormatter
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Commands')
        
        # Scan command
        scan_parser = subparsers.add_parser('scan', help='Run security scans')
        scan_parser.add_argument('-u', '--url', help='Target URL to scan')
        scan_parser.add_argument('-t', '--type', choices=self.scanners.keys(), 
                                help='Type of scan to perform')
        scan_parser.add_argument('-a', '--all', action='store_true', 
                                help='Run all scan types')
        scan_parser.add_argument('-o', '--output', help='Output file for results')
        scan_parser.add_argument('-f', '--format', choices=['json', 'html', 'txt'], default='json',
                                help='Output format (default: json)')
        scan_parser.add_argument('-v', '--verbose', action='store_true',
                                help='Enable verbose output')
        scan_parser.add_argument('-d', '--delay', type=float, default=0.5,
                                help='Delay between requests in seconds (default: 0.5)')
        
        # Profile command
        profile_parser = subparsers.add_parser('profile', help='Manage scan profiles')
        profile_subparsers = profile_parser.add_subparsers(dest='profile_command')
        
        list_profile = profile_subparsers.add_parser('list', help='List available profiles')
        
        create_profile = profile_subparsers.add_parser('create', help='Create a new profile')
        create_profile.add_argument('-n', '--name', required=True, help='Profile name')
        create_profile.add_argument('-t', '--types', nargs='+', choices=self.scanners.keys(),
                                   help='Scan types to include')
        
        run_profile = profile_subparsers.add_parser('run', help='Run a saved profile')
        run_profile.add_argument('-n', '--name', required=True, help='Profile name')
        run_profile.add_argument('-u', '--url', required=True, help='Target URL')
        run_profile.add_argument('-o', '--output', help='Output file for results')
        run_profile.add_argument('-f', '--format', choices=['json', 'html', 'txt'], default='json',
                                help='Output format (default: json)')
        
        # Plugin command
        plugin_parser = subparsers.add_parser('plugin', help='Manage plugins')
        plugin_subparsers = plugin_parser.add_subparsers(dest='plugin_command')
        
        update_plugins = plugin_subparsers.add_parser('update', help='Update plugins from GitHub')
        list_plugins = plugin_subparsers.add_parser('list', help='List installed plugins')
        add_plugin = plugin_subparsers.add_parser('add', help='Add a new plugin')
        add_plugin.add_argument('-n', '--name', required=True, help='Plugin name')
        add_plugin.add_argument('-r', '--repo', required=True, help='GitHub repository URL')
        add_plugin.add_argument('-b', '--branch', default='main', help='Repository branch (default: main)')
        
        # Interactive mode
        interactive_parser = subparsers.add_parser('interactive', help='Run in interactive mode')
        
        return parser
    
    def run(self):
        self.display_banner()
        parser = self.setup_argparse()
        args = parser.parse_args()
        
        if not args.command:
            parser.print_help()
            return
            
        if args.command == 'scan':
            self._handle_scan_command(args)
        elif args.command == 'profile':
            self._handle_profile_command(args)
        elif args.command == 'plugin':
            self._handle_plugin_command(args)
        elif args.command == 'interactive':
            self._run_interactive_mode()
    
    def _handle_scan_command(self, args):
        if not args.url and not (args.command == 'profile' and args.profile_command == 'list'):
            console.print("[bold red]Error:[/bold red] URL is required for scanning")
            return
            
        results = {}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            if args.all:
                task = progress.add_task("[green]Running all scans...", total=len(self.scanners))
                for scanner_name, scanner in self.scanners.items():
                    # Skip the special 'xss-all' case
                    if scanner_name == 'xss-all':
                        continue
                        
                    progress.update(task, description=f"[green]Running {scanner_name} scan...")
                    if scanner_name.startswith('xss-') and args.verbose:
                        console.print(f"\n[bold cyan]Running {scanner_name} scan with verbose output:[/bold cyan]")
                    
                    results[scanner_name] = scanner.scan(args.url, verbose=args.verbose, delay=args.delay)
                    progress.update(task, advance=1)
                    time.sleep(0.5)  # Small delay for UI
                    
            elif args.type:
                if args.type == 'xss-all':
                    # Run all XSS scanners
                    xss_scanners = {k: v for k, v in self.scanners.items() if k.startswith('xss-') and k != 'xss-all'}
                    task = progress.add_task("[green]Running all XSS scans...", total=len(xss_scanners))
                    
                    for scanner_name, scanner in xss_scanners.items():
                        progress.update(task, description=f"[green]Running {scanner_name} scan...")
                        if args.verbose:
                            console.print(f"\n[bold cyan]Running {scanner_name} scan with verbose output:[/bold cyan]")
                        results[scanner_name] = scanner.scan(args.url, verbose=args.verbose, delay=args.delay)
                        progress.update(task, advance=1)
                        time.sleep(0.5)  # Small delay for UI
                else:
                    # Run a single scanner
                    task = progress.add_task(f"[green]Running {args.type} scan...", total=1)
                    if args.verbose:
                        console.print(f"\n[bold cyan]Running {args.type} scan with verbose output:[/bold cyan]")
                    results[args.type] = self.scanners[args.type].scan(args.url, verbose=args.verbose, delay=args.delay)
                    progress.update(task, advance=1)
            else:
                console.print("[bold red]Error:[/bold red] Please specify a scan type or use --all")
                return
                
        self._output_results(results, args.output, args.format, args.url)
    
    def _handle_profile_command(self, args):
        if not args.profile_command:
            console.print("[bold red]Error:[/bold red] Please specify a profile subcommand")
            return
            
        if args.profile_command == 'list':
            profiles = self.profile_manager.list_profiles()
            if profiles:
                table = Table(title="Available Scan Profiles")
                table.add_column("Profile Name", style="cyan")
                table.add_column("Scan Types", style="green")
                table.add_column("Created At", style="dim")
                
                for profile in profiles:
                    table.add_row(
                        profile['name'],
                        ", ".join(profile['scan_types']),
                        profile.get('created_at', 'Unknown')
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No profiles found[/yellow]")
                
        elif args.profile_command == 'create':
            if not args.types:
                console.print("[bold red]Error:[/bold red] Please specify scan types to include in the profile")
                return
                
            with console.status("[bold green]Creating profile..."):
                success = self.profile_manager.create_profile(args.name, args.types)
            
            if success:
                console.print(f"[bold green]Profile '{args.name}' created successfully[/bold green]")
            else:
                console.print(f"[bold red]Error creating profile '{args.name}'[/bold red]")
                
        elif args.profile_command == 'run':
            profile = self.profile_manager.get_profile(args.name)
            if not profile:
                console.print(f"[bold red]Error:[/bold red] Profile '{args.name}' not found")
                return
                
            results = {}
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                console=console
            ) as progress:
                task = progress.add_task(f"[green]Running profile '{args.name}'...", total=len(profile['scan_types']))
                
                for scan_type in profile['scan_types']:
                    progress.update(task, description=f"[green]Running {scan_type} scan...")
                    
                    if scan_type == 'xss-all':
                        # Handle the special case for all XSS scans
                        xss_scanners = {k: v for k, v in self.scanners.items() if k.startswith('xss-') and k != 'xss-all'}
                        for xss_scanner_name, xss_scanner in xss_scanners.items():
                            results[xss_scanner_name] = xss_scanner.scan(args.url)
                    else:
                        results[scan_type] = self.scanners[scan_type].scan(args.url)
                    
                    progress.update(task, advance=1)
                    time.sleep(0.5)  # Small delay for UI
                
            self._output_results(results, args.output, args.format, args.url)
    
    def _handle_plugin_command(self, args):
        if not args.plugin_command:
            console.print("[bold red]Error:[/bold red] Please specify a plugin subcommand")
            return
            
        if args.plugin_command == 'update':
            with console.status("[bold green]Updating plugins from GitHub..."):
                updated = self.plugin_updater.update_plugins()
            
            console.print(f"[bold green]Updated {updated} plugins[/bold green]")
            
        elif args.plugin_command == 'list':
            plugins = self.plugin_updater.list_plugins()
            if plugins:
                table = Table(title="Installed Plugins")
                table.add_column("Plugin Name", style="cyan")
                table.add_column("Version", style="green")
                table.add_column("Repository", style="blue")
                table.add_column("Last Updated", style="dim")
                
                for plugin in plugins:
                    table.add_row(
                        plugin['name'],
                        plugin.get('version', 'Unknown'),
                        plugin.get('repo_url', 'Unknown'),
                        plugin.get('updated_at', 'Unknown')
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No plugins installed[/yellow]")
                
        elif args.plugin_command == 'add':
            with console.status(f"[bold green]Adding plugin '{args.name}' from {args.repo}..."):
                success = self.plugin_updater.add_plugin(args.name, args.repo, args.branch)
            
            if success:
                console.print(f"[bold green]Plugin '{args.name}' added successfully[/bold green]")
            else:
                console.print(f"[bold red]Error adding plugin '{args.name}'[/bold red]")
    
    def _run_interactive_mode(self):
        console.print("[bold cyan]Welcome to CyberNexus Interactive Mode![/bold cyan]")
        console.print("[dim]This mode will guide you through the scanning process.[/dim]\n")
        
        # Get target URL
        url = Prompt.ask("[bold]Enter target URL to scan[/bold]", default="https://evil.com")
        
        # Select scan types
        console.print("\n[bold]Available scan types:[/bold]")
        for i, scan_type in enumerate(self.scanners.keys(), 1):
            console.print(f"  {i}. [cyan]{scan_type}[/cyan]")
        
        console.print(f"  {len(self.scanners) + 1}. [green]All scans[/green]")
        
        choice = Prompt.ask("[bold]Select scan type (number or name)[/bold]", default="all")
        
        # Process choice
        scan_types = []
        if choice.lower() == "all" or choice == str(len(self.scanners) + 1):
            scan_types = list(self.scanners.keys())
            # Remove the special 'xss-all' case as we'll run individual XSS scans
            if 'xss-all' in scan_types:
                scan_types.remove('xss-all')
        elif choice.isdigit() and 1 <= int(choice) <= len(self.scanners):
            scan_type = list(self.scanners.keys())[int(choice) - 1]
            scan_types = [scan_type]
        elif choice in self.scanners:
            scan_types = [choice]
        else:
            console.print("[bold red]Invalid selection. Running all scans.[/bold red]")
            scan_types = list(self.scanners.keys())
            if 'xss-all' in scan_types:
                scan_types.remove('xss-all')
        
        # Ask for output options
        save_output = Confirm.ask("[bold]Save results to file?[/bold]", default=True)
        output_file = None
        output_format = "json"
        
        if save_output:
            output_file = Prompt.ask("[bold]Enter output filename[/bold]", default="cybernexus_results")
            output_format = Prompt.ask(
                "[bold]Select output format[/bold]",
                choices=["json", "html", "txt"],
                default="html"
            )
            
            # Add extension if not provided
            if not output_file.endswith(f".{output_format}"):
                output_file = f"{output_file}.{output_format}"
        
        # Ask for verbose mode
        verbose = Confirm.ask("[bold]Enable verbose output?[/bold]", default=False)
        
        # Ask for request delay
        delay = float(Prompt.ask(
            "[bold]Enter delay between requests (seconds)[/bold]",
            default="0.5"
        ))
        
        # Run the scans
        results = {}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[green]Running scans...", total=len(scan_types))
            
            for scan_type in scan_types:
                progress.update(task, description=f"[green]Running {scan_type} scan...")
                
                if scan_type == 'xss-all':
                    # Handle the special case for all XSS scans
                    xss_scanners = {k: v for k, v in self.scanners.items() if k.startswith('xss-') and k != 'xss-all'}
                    for xss_scanner_name, xss_scanner in xss_scanners.items():
                        results[xss_scanner_name] = xss_scanner.scan(url, verbose=verbose, delay=delay)
                else:
                    results[scan_type] = self.scanners[scan_type].scan(url, verbose=verbose, delay=delay)
                
                progress.update(task, advance=1)
                time.sleep(0.5)  # Small delay for UI
        
        # Output results
        self._output_results(results, output_file, output_format, url)
    
    def _output_results(self, results, output_file=None, output_format="json", target_url=None):
        # First, display results in the console
        console.print("\n[bold green]Scan Results:[/bold green]")
        
        # Create a tree view of results
        tree = Tree("[bold]Scan Summary[/bold]")
        
        total_issues = 0
        high_issues = 0
        medium_issues = 0
        low_issues = 0
        
        for scan_type, scan_results in results.items():
            if isinstance(scan_results, list):
                scan_node = tree.add(f"[cyan]{scan_type}[/cyan]: {len(scan_results)} findings")
                
                # Count issues by severity
                for issue in scan_results:
                    total_issues += 1
                    if "high" in issue.lower():
                        high_issues += 1
                    elif "medium" in issue.lower():
                        medium_issues += 1
                    else:
                        low_issues += 1
                    
                    if "vulnerability found" in issue.lower() or "vulnerable" in issue.lower():
                        scan_node.add(f"[bold red]{issue}[/bold red]")
                    elif "warning" in issue.lower():
                        scan_node.add(f"[bold yellow]{issue}[/bold yellow]")
                    else:
                        scan_node.add(f"[dim]{issue}[/dim]")
                        
            elif isinstance(scan_results, dict):
                scan_node = tree.add(f"[cyan]{scan_type}[/cyan]")
                
                if "vulnerable" in scan_results and scan_results["vulnerable"]:
                    scan_node.add("[bold red]Vulnerable: Yes[/bold red]")
                    high_issues += 1
                    total_issues += 1
                elif "vulnerable" in scan_results:
                    scan_node.add("[green]Vulnerable: No[/green]")
                
                for key, value in scan_results.items():
                    if key != "vulnerable" and key != "details":
                        scan_node.add(f"[blue]{key}[/blue]: {value}")
                
                if "details" in scan_results and isinstance(scan_results["details"], list):
                    details_node = scan_node.add("[bold]Details:[/bold]")
                    for detail in scan_results["details"]:
                        if "error" in detail.lower() or "vulnerable" in detail.lower():
                            details_node.add(f"[bold red]{detail}[/bold red]")
                        elif "warning" in detail.lower():
                            details_node.add(f"[bold yellow]{detail}[/bold yellow]")
                        elif "recommendation" in detail.lower():
                            details_node.add(f"[bold green]{detail}[/bold green]")
                        else:
                            details_node.add(f"{detail}")
        
        # Add summary information
        summary_node = tree.add("[bold]Summary[/bold]")
        summary_node.add(f"[bold]Total Issues:[/bold] {total_issues}")
        summary_node.add(f"[bold red]High Severity:[/bold red] {high_issues}")
        summary_node.add(f"[bold yellow]Medium Severity:[/bold yellow] {medium_issues}")
        summary_node.add(f"[bold blue]Low Severity:[/bold blue] {low_issues}")
        
        console.print(tree)
        
        # Save results to file if requested
        if output_file:
            with console.status(f"[bold green]Saving results to {output_file}..."):
                # Add metadata to results
                full_results = {
                    "metadata": {
                        "scanner": "CyberNexus",
                        "target": target_url,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "summary": {
                            "total_issues": total_issues,
                            "high_severity": high_issues,
                            "medium_severity": medium_issues,
                            "low_severity": low_issues
                        }
                    },
                    "results": results
                }
                
                success = self.report_generator.generate_report(full_results, output_file, output_format)
                
                if success:
                    console.print(f"[bold green]Results saved to {output_file}[/bold green]")
                else:
                    console.print(f"[bold red]Error saving results to {output_file}[/bold red]")

if __name__ == "__main__":
    try:
        scanner = CyberNexus()
        scanner.run()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Scan interrupted by user[/bold yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)