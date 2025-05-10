import argparse
from rich.console import Console
from core import scanner
from plugins import load_plugins

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Cyber Nexus CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser("scan", help="Scan a single URL")
    scan_parser.add_argument("--url", required=True, help="Target URL")
    scan_parser.set_defaults(func=scanner.run)

    # Load external plugins
    load_plugins(subparsers)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
