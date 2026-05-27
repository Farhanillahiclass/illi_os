import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

import pyautogui
from PIL import Image

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
except ImportError:
    sync_playwright = None
    PlaywrightTimeoutError = Exception

BASE_DIR = Path(__file__).resolve().parent
BROWSER_PROFILE = BASE_DIR / ".cache" / "browser_profile"
SCREENSHOT_DIR = BASE_DIR / "screenshots"
DATA_DIR = BASE_DIR / "md_reports"

for folder in (BROWSER_PROFILE, SCREENSHOT_DIR, DATA_DIR):
    folder.mkdir(parents=True, exist_ok=True)


def safe_filename(text: str) -> str:
    safe = "".join(c for c in text if c.isalnum() or c in "-_ .").strip()
    return safe[:120] if len(safe) > 120 else safe


def launch_persistent_browser(headless: bool = False):
    if sync_playwright is None:
        raise RuntimeError("Playwright is not installed. Install via pip and run `playwright install`.")
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch_persistent_context(user_data_dir=str(BROWSER_PROFILE), headless=headless)
    return playwright, browser


def capture_screenshot(page, label: str = "ui") -> Path:
    target = SCREENSHOT_DIR / f"{label}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.png"
    page.screenshot(path=str(target), full_page=True)
    return target


def simulate_input(page, selector: str, text: str):
    element = page.query_selector(selector)
    if element:
        try:
            element.click()
            element.fill(text)
            return True
        except Exception:
            pass
    return False


def compute_button_coordinates(page, selector: str):
    element = page.query_selector(selector)
    if not element:
        return None
    box = element.bounding_box()
    if not box:
        return None
    return int(box["x"] + box["width"] / 2), int(box["y"] + box["height"] / 2)


def write_markdown(prompt: str, url: str, extracted: str, screenshot_path: Path, output_name: str = None) -> Path:
    filename = output_name or safe_filename(prompt or "illi_scrape")
    md_file = DATA_DIR / f"{filename}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.md"
    with open(md_file, "w", encoding="utf-8") as handle:
        handle.write(f"# ILLI OS Capture Report\n")
        handle.write(f"**Prompt:** {prompt}\n\n")
        handle.write(f"**Source URL:** {url}\n\n")
        handle.write(f"**Captured:**\n\n```\n{extracted}\n```\n\n")
        handle.write(f"**Screenshot:** {screenshot_path.name}\n")
        handle.write(f"**Generated:** {datetime.utcnow().isoformat()}Z\n")
    try:
        if sys.platform.startswith("win"):
            os.startfile(md_file)
        else:
            subprocess.Popen(["xdg-open", str(md_file)])
    except Exception:
        pass
    return md_file


def scrape_to_markdown(prompt: str, url: str, selector: str = "body", output_name: str = None) -> Path:
    if sync_playwright is None:
        raise RuntimeError("Playwright is required for browser automation.")
    playwright, browser = launch_persistent_browser(headless=False)
    try:
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(1800)
        screenshot = capture_screenshot(page, "scrape")
        extracted = ""
        try:
            extracted = page.inner_text(selector)
        except Exception:
            extracted = page.content()
        write_markdown(prompt, url, extracted, screenshot, output_name)
        return screenshot
    finally:
        browser.close()
        playwright.stop()


def read_voice_script(timeout: int = 6) -> str:
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.9)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=timeout)
            return recognizer.recognize_sphinx(audio)
    except Exception as exc:
        return f"Voice capture unavailable: {exc}"


def open_whatsapp_persistent():
    if sync_playwright is None:
        raise RuntimeError("Playwright is required for WhatsApp automation.")
    playwright, browser = launch_persistent_browser(headless=False)
    try:
        page = browser.new_page()
        page.goto("https://web.whatsapp.com", wait_until="networkidle")
        page.wait_for_timeout(2500)
        capture_screenshot(page, "whatsapp_home")
        return page
    finally:
        browser.close()
        playwright.stop()


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--launch-whatsapp":
        print("Launching WhatsApp Web with persistent local browser profile...")
        open_whatsapp_persistent()
        return
    if len(sys.argv) > 1 and sys.argv[1] == "--scrape":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "Browser scrape"
        url = sys.argv[3] if len(sys.argv) > 3 else "https://example.com"
        selector = sys.argv[4] if len(sys.argv) > 4 else "body"
        scrape_to_markdown(prompt, url, selector)
        return
    print("Usage: python browser_agent.py --launch-whatsapp | --scrape <prompt> <url> [selector]")


if __name__ == "__main__":
    main()
