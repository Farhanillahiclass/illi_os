import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from illi_ai.assistant import dispatch_command, get_installed_apps


def main():
    parser = argparse.ArgumentParser(description="ILLI OS Assistant Command Dispatcher")
    parser.add_argument("--command", "-c", help="Text command to execute", type=str)
    parser.add_argument("--list-apps", action="store_true", help="List discovered installed applications")
    parser.add_argument("--scan-apps", action="store_true", help="Scan for installed applications and display count")
    args = parser.parse_args()

    if args.list_apps or args.scan_apps:
        apps = get_installed_apps(force_refresh=args.scan_apps)
        print(f"Discovered {len(apps)} installed apps.")
        if args.list_apps:
            for name, path in sorted(apps.items(), key=lambda item: item[0]):
                print(f"- {name}: {path}")
        return

    if args.command:
        result = dispatch_command(args.command)
        print(result.get("message", "No output. "))
        if result.get("url"):
            print(f"Opened URL: {result['url']}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
