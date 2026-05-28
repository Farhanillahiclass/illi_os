import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent # Adjust for new illi/cli.py location


def main():
    if "--launch" in sys.argv:
        subprocess.run([sys.executable, str(BASE_DIR / "ui" / "app.py")], check=False)
        return
    print("Usage: illi --launch")
    print("This command starts the ILLI AI Operating System HUD.")
