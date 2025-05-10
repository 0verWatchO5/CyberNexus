from core.profile_runner import run_profile

def run(args):
    run_profile(args.file)

def register(subparsers):
    parser = subparsers.add_parser("profile-scan", help="Scan targets from a profile JSON")
    parser.add_argument("--file", required=True, help="Path to profile file")
    parser.set_defaults(func=run)
