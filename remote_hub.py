import asyncio
import json
import os
import re
import smtplib
import subprocess
import time
from datetime import datetime
from pathlib import Path

import psutil
import speech_recognition as sr

BASE_DIR = Path(__file__).resolve().parent
INBOX_DIR = BASE_DIR / "remote_inbox"
OUTBOX_DIR = BASE_DIR / "remote_outbox"
TRUSTED_FILE = BASE_DIR / "trusted_contacts.json"

for folder in (INBOX_DIR, OUTBOX_DIR):
    folder.mkdir(exist_ok=True)

DEFAULT_TRUSTED = {
    "trusted_numbers": ["+10000000000"],
    "trusted_names": ["ILLIGENT"]
}


def load_trusted_contacts():
    if TRUSTED_FILE.exists():
        try:
            return json.loads(TRUSTED_FILE.read_text(encoding="utf-8"))
        except Exception:
            return DEFAULT_TRUSTED
    TRUSTED_FILE.write_text(json.dumps(DEFAULT_TRUSTED, indent=2), encoding="utf-8")
    return DEFAULT_TRUSTED


def classify_instruction(payload: str) -> str:
    text = payload.lower()
    if any(key in text for key in ["clear recycle", "empty recycle", "recycle bin"]):
        return "clear_recycle_bin"
    if any(key in text for key in ["send email", "email draft", "compose email"]):
        return "send_email_draft"
    if any(key in text for key in ["snapshot", "system activity", "status report"]):
        return "system_snapshot"
    if any(key in text for key in ["lock machine", "lock workstation", "secure lock"]):
        return "lock_workstation"
    if any(key in text for key in ["run diagnostics", "diagnostic", "health check"]):
        return "system_diagnostic"
    return "unknown"


def clear_recycle_bin() -> str:
    if os.name == "nt":
        subprocess.run(["powershell.exe", "-NoProfile", "-Command", "Clear-RecycleBin -Force"], check=False)
        return "Recycle bin cleared locally."
    return "Recycle bin clear is only supported on Windows environments."


def send_email_draft(payload: str) -> str:
    draft_folder = BASE_DIR / "email_drafts"
    draft_folder.mkdir(exist_ok=True)
    draft_file = draft_folder / f"draft_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(draft_file, "w", encoding="utf-8") as handle:
        handle.write("ILLI OS Email Draft\n")
        handle.write(f"Generated: {datetime.utcnow().isoformat()}Z\n")
        handle.write("---\n")
        handle.write(payload)
    try:
        with smtplib.SMTP("localhost", 25, timeout=4) as smtp:
            smtp.noop()
        return f"Email draft saved: {draft_file.name} and local SMTP available."
    except Exception:
        return f"Email draft saved: {draft_file.name}. Local SMTP unavailable, draft stored for later delivery."


def system_snapshot(payload: str) -> str:
    snapshot_file = BASE_DIR / "logs" / f"remote_snapshot_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"
    snapshot_file.parent.mkdir(exist_ok=True)
    with open(snapshot_file, "w", encoding="utf-8") as handle:
        handle.write(f"Timestamp: {datetime.utcnow().isoformat()}Z\n")
        handle.write(f"CPU: {psutil.cpu_percent()}%\n")
        handle.write(f"Memory: {psutil.virtual_memory().percent}%\n")
        handle.write(f"Disk C: {psutil.disk_usage('C:\\' if os.name=='nt' else '/').percent}%\n")
        net = psutil.net_io_counters()
        handle.write(f"Network: {net.bytes_recv / 1024:.2f} KB recv, {net.bytes_sent / 1024:.2f} KB sent\n")
    return f"System snapshot written to {snapshot_file.name}."


def lock_workstation() -> str:
    if os.name == "nt":
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], check=False)
        return "Workstation lock requested."
    return "Lock command only supported on Windows."


def system_diagnostic() -> str:
    diag_file = BASE_DIR / "logs" / f"remote_diagnostic_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"
    diag_file.parent.mkdir(exist_ok=True)
    with open(diag_file, "w", encoding="utf-8") as handle:
        handle.write(f"ILLI OS Remote Diagnostic\nTimestamp: {datetime.utcnow().isoformat()}Z\n\n")
        handle.write(f"CPU cores: {psutil.cpu_count(logical=True)}\n")
        handle.write(f"Uptime: {time_uptime()}\n")
        handle.write(f"Memory: {psutil.virtual_memory()}\n")
        handle.write(f"Disk partitions: {psutil.disk_partitions()}\n")
    return f"Remote system diagnostic saved to {diag_file.name}."


def time_uptime() -> str:
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    return str(uptime).split('.')[0]


def classify_and_execute(payload: str) -> str:
    command = classify_instruction(payload)
    if command == "clear_recycle_bin":
        return clear_recycle_bin()
    if command == "send_email_draft":
        return send_email_draft(payload)
    if command == "system_snapshot":
        return system_snapshot(payload)
    if command == "lock_workstation":
        return lock_workstation()
    if command == "system_diagnostic":
        return system_diagnostic()
    return "No valid remote directive detected."


def parse_incoming_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    contact = None
    if "From:" in text:
        match = re.search(r"From:\s*(.+)", text)
        if match:
            contact = match.group(1).strip()
    content = text.strip()
    return {"source": contact or path.stem, "payload": content}


def transcribe_audio(path: Path) -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(str(path)) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_sphinx(audio)
    except Exception as exc:
        return f"Audio transcription failed: {exc}"


def publish_summary(source: str, summary: str, original: str):
    out_name = OUTBOX_DIR / f"reply_{source}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(out_name, "w", encoding="utf-8") as handle:
        handle.write(f"Source: {source}\n")
        handle.write(f"Timestamp: {datetime.utcnow().isoformat()}Z\n")
        handle.write("---\n")
        handle.write(f"Original Payload:\n{original}\n\n")
        handle.write(f"Summary:\n{summary}\n")
    return out_name


async def monitor_inbox():
    trusted = load_trusted_contacts()
    processed = set()
    while True:
        for path in INBOX_DIR.iterdir():
            if path.name in processed or path.is_dir():
                continue
            if path.suffix.lower() in {".txt", ".md"}:
                incoming = parse_incoming_file(path)
            elif path.suffix.lower() in {".wav", ".mp3", ".flac"}:
                incoming = {"source": path.stem, "payload": transcribe_audio(path)}
            else:
                continue
            sender = incoming.get("source", "unknown")
            if sender not in trusted.get("trusted_numbers", []) and sender not in trusted.get("trusted_names", []):
                processed.add(path.name)
                continue
            summary = classify_and_execute(incoming["payload"])
            publish_summary(sender, summary, incoming["payload"])
            processed.add(path.name)
        await asyncio.sleep(5)


def main():
    print("ILLI OS Remote Gateway Terminal starting...")
    try:
        asyncio.run(monitor_inbox())
    except KeyboardInterrupt:
        print("Remote terminal worker stopped.")


if __name__ == "__main__":
    main()
