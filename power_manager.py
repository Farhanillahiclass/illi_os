"""Deep OS Overlord: Administrative-level OS control for ILLI."""
import subprocess
import platform
import ctypes
from ctypes import wintypes
import os


def sleep():
    if platform.system() != 'Windows':
        raise RuntimeError('Windows only')
    # Use SetSuspendState via powrprof
    subprocess.Popen(["rundll32.exe", "powrprof.dll,SetSuspendState 0,1,0"], shell=False)


def restart():
    if platform.system() != 'Windows':
        raise RuntimeError('Windows only')
    subprocess.Popen(["shutdown", "/r", "/t", "0"], shell=False)


def shutdown():
    if platform.system() != 'Windows':
        raise RuntimeError('Windows only')
    subprocess.Popen(["shutdown", "/s", "/t", "0"], shell=False)


def clear_recycle_bin():
    if platform.system() != 'Windows':
        raise RuntimeError('Windows only')
    try:
        shell32 = ctypes.windll.shell32
        SHERB_NOCONFIRMATION = 0x00000001
        SHEmptyRecycleBin = shell32.SHEmptyRecycleBinW
        SHEmptyRecycleBin(None, None, SHERB_NOCONFIRMATION)
        return True
    except Exception:
        return False


class DeepOSOverlordPowerManager:
    """
    Direct administrative-level OS control.
    Wallpaper, Sleep, Reboot, Shutdown, Audio Mute, Recycle Bin, System Scan.
    """

    @staticmethod
    def sleep_system() -> bool:
        """Put system to sleep."""
        return sleep()

    @staticmethod
    def restart_system(delay_seconds: int = 5) -> bool:
        """Restart system with delay."""
        try:
            subprocess.run(["shutdown", "/r", "/t", str(delay_seconds)], check=True)
            return True
        except Exception:
            return False

    @staticmethod
    def shutdown_system(delay_seconds: int = 5) -> bool:
        """Shutdown system with delay."""
        try:
            subprocess.run(["shutdown", "/s", "/t", str(delay_seconds)], check=True)
            return True
        except Exception:
            return False

    @staticmethod
    def clear_recycle_bin() -> bool:
        """Permanently clear Windows Recycle Bin."""
        return clear_recycle_bin()

    @staticmethod
    def launch_application(app_name: str) -> bool:
        """Launch application by name or path."""
        if not app_name:
            return False
        try:
            subprocess.Popen(app_name, shell=True) # Use shell=True for broader app launching
            return True
        except FileNotFoundError:
            # Try searching in PATH
            from shutil import which
            app_path = which(app_name)
            if app_path:
                subprocess.Popen(app_path, shell=True)
                return True
        except Exception:
            pass
        return False

    @staticmethod
    def run_system_scan_report() -> str:
        # This will be moved to a dedicated diagnostics module later
        return "System scan report placeholder."
