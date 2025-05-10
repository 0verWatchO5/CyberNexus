from utils.update_plugins import update_all_plugins

def run(args):
    update_all_plugins()

def register(subparsers):
    parser = subparsers.add_parser("update-all", help="Auto-update all plugins from GitHub")
    parser.set_defaults(func=run)
