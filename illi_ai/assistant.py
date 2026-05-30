import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Optional, List, Any
from urllib.parse import quote_plus
import webbrowser

import requests

_installed_apps_cache: Optional[Dict[str, str]] = None

SEARCH_DIRECTORIES = [
    os.environ.get("PROGRAMFILES", ""),
    os.environ.get("PROGRAMFILES(X86)", ""),
    os.environ.get("LOCALAPPDATA", ""),
    os.environ.get("APPDATA", ""),
    os.environ.get("PROGRAMDATA", ""),
]

START_MENU_DIRS = [
    Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs",
    Path(os.environ.get("PROGRAMDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs",
]

YOUTUBE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


def normalize_app_name(name: str) -> str:
    if not name:
        return ""
    path_name = Path(name).stem if Path(name).suffix else name
    normalized = re.sub(r"[^a-z0-9]+", " ", path_name.lower()).strip()
    return normalized


def _add_candidate(app_map: Dict[str, str], file_path: Path) -> None:
    key = normalize_app_name(file_path.stem)
    if key and key not in app_map:
        app_map[key] = str(file_path)


def discover_installed_apps(max_entries: int = 1500) -> Dict[str, str]:
    apps: Dict[str, str] = {}

    # Add PATH executables first
    for path_dir in os.environ.get("PATH", "").split(os.pathsep):
        if not path_dir:
            continue
        try:
            for item in Path(path_dir).iterdir():
                if item.is_file() and item.suffix.lower() in {".exe", ".cmd", ".bat"}:
                    _add_candidate(apps, item)
        except Exception:
            continue

    # Scan program directories and start menu shortcuts
    search_dirs = [Path(d) for d in SEARCH_DIRECTORIES if d]
    search_dirs.extend([path for path in START_MENU_DIRS if path.exists()])
    scanned = 0

    for root_dir in search_dirs:
        if not root_dir.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if scanned >= max_entries:
                    break
                lower = filename.lower()
                if lower.endswith(('.exe', '.lnk', '.appref-ms', '.bat', '.cmd')):
                    _add_candidate(apps, Path(dirpath) / filename)
                    scanned += 1
            if scanned >= max_entries:
                break
        if scanned >= max_entries:
            break

    return apps


def get_installed_apps(force_refresh: bool = False) -> Dict[str, str]:
    global _installed_apps_cache
    if _installed_apps_cache is None or force_refresh:
        _installed_apps_cache = discover_installed_apps()
    return _installed_apps_cache


def resolve_app_path(app_name: str, app_map: Optional[Dict[str, str]] = None) -> Optional[str]:
    if not app_name:
        return None
    if os.path.exists(app_name):
        return str(Path(app_name).resolve())

    normalized = normalize_app_name(app_name)
    if not normalized:
        return None

    app_map = app_map or get_installed_apps()
    if normalized in app_map:
        return app_map[normalized]

    matches = []
    for key, path in app_map.items():
        if normalized in key:
            matches.append((key, path))

    if matches:
        matches.sort(key=lambda item: len(item[0]))
        return matches[0][1]

    search_terms = normalized.split()
    for key, path in app_map.items():
        if all(term in key for term in search_terms):
            return path

    return None


def open_application(app_name: str) -> bool:
    target = resolve_app_path(app_name)
    if target:
        try:
            os.startfile(target)
            return True
        except Exception:
            pass
    try:
        subprocess.Popen(app_name, shell=False)
        return True
    except Exception:
        try:
            subprocess.Popen(["cmd", "/c", "start", "", app_name], shell=False)
            return True
        except Exception:
            return False


def find_youtube_video(query: str) -> Optional[str]:
    if not query:
        return None
    search_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
    try:
        response = requests.get(search_url, headers=YOUTUBE_HEADERS, timeout=10)
        response.raise_for_status()
        html = response.text
        matches = re.findall(r"/watch\?v=[\w-]+", html)
        if matches:
            return f"https://www.youtube.com{matches[0]}"
    except Exception:
        pass
    return search_url


def open_file(file_path: str) -> bool:
    if not file_path:
        return False
    target = Path(file_path).expanduser()
    if not target.exists():
        return False
    try:
        os.startfile(str(target))
        return True
    except Exception:
        return False


def create_directory(directory_path: str) -> bool:
    if not directory_path:
        return False
    target = Path(directory_path).expanduser()
    try:
        target.mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


def create_file(file_path: str, content: Optional[str] = None) -> bool:
    if not file_path:
        return False
    target = Path(file_path).expanduser()
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        if content is not None:
            target.write_text(content, encoding="utf-8")
        else:
            target.touch(exist_ok=True)
        return True
    except Exception:
        return False


def delete_path(path: str) -> bool:
    if not path:
        return False
    target = Path(path).expanduser()
    if not target.exists():
        return False
    try:
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()
        return True
    except Exception:
        return False


def dispatch_command(command: str) -> Dict[str, Any]:
    normalized = command.lower().strip()
    if not normalized:
        return {"success": False, "message": "No command provided."}

    if "play video" in normalized or "youtube" in normalized:
        query = normalized
        for prefix in ["play video", "play youtube", "youtube", "search youtube for"]:
            if prefix in query:
                query = query.split(prefix, 1)[-1].strip()
                break
        if not query:
            query = "trending videos"
        target = find_youtube_video(query)
        if target:
            webbrowser.open_new_tab(target)
            return {"success": True, "message": f"Opening YouTube video: {target}", "url": target}
        return {"success": False, "message": "Unable to find a video for that query."}

    create_match = re.search(r"(?:create|make|new)\s+(?:file|folder|directory)\s+(.+)", normalized)
    if create_match:
        path = create_match.group(1).strip().strip('"')
        if "folder" in normalized or "directory" in normalized:
            success = create_directory(path)
            return {"success": success, "message": f"Created directory: {path}" if success else f"Failed to create directory: {path}"}
        success = create_file(path)
        return {"success": success, "message": f"Created file: {path}" if success else f"Failed to create file: {path}"}

    delete_match = re.search(r"(?:delete|remove|rm)\s+(?:file|folder|directory)\s+(.+)", normalized)
    if delete_match:
        path = delete_match.group(1).strip().strip('"')
        success = delete_path(path)
        return {"success": success, "message": f"Deleted: {path}" if success else f"Failed to delete: {path}"}

    open_file_match = re.search(r"(?:open|view|show)\s+(?:file|document|folder|directory)\s+(.+)", normalized)
    if open_file_match:
        path = open_file_match.group(1).strip().strip('"')
        success = open_file(path)
        return {"success": success, "message": f"Opened: {path}" if success else f"Failed to open: {path}"}

    launch_match = re.search(r"(?:launch|open|start)\s+(.+)", normalized)
    if launch_match:
        app_name = launch_match.group(1).strip().strip('"')
        if app_name:
            success = open_application(app_name)
            return {"success": success, "message": f"Launching: {app_name}" if success else f"Unable to launch: {app_name}"}

    return {"success": False, "message": "Command not recognized. Try commands like 'open calculator', 'play video lofi beats', 'create file notes.txt', or 'delete folder temp'."}
