"""
ILLI Application Launcher: Scans local paths and safely launches software.
"""
import subprocess
import os
from shutil import which

def launch_application(app_name: str) -> bool:
    """Launch application by name or path."""
    if not app_name:
        return False
    try:
        subprocess.Popen(app_name, shell=True) # Use shell=True for broader app launching
        return True
    except FileNotFoundError:
        app_path = which(app_name)
        if app_path:
            subprocess.Popen(app_path, shell=True)
            return True
    except Exception:
        pass
    return False