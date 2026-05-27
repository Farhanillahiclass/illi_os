import os
import threading
from datetime import datetime, timezone
from pathlib import Path

import psutil
import pyttsx3
import speech_recognition as sr
import streamlit as st

from illi_ai.hotkeys import start_listener
from illi_ai.power import clear_recycle_bin, restart, shutdown, sleep
from illi_ai.wallpaper import generate_hex_grid, set_wallpaper

try:
    import browser_agent
except ImportError:
    browser_agent = None

try:
    from ctypes import POINTER, cast
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
except Exception:
    AudioUtilities = None
    IAudioEndpointVolume = None
    CLSCTX_ALL = None

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

MIC_STATE_KEY = "mic_live"
LOG_STATE_KEY = "log_lines"
NET_STATE_KEY = "network_history"
NET_LAST_KEY = "net_last"
STATUS_MESSAGE_KEY = "status_message"
WALLPAPER_PROFILE_KEY = "wallpaper_profile"
VOICE_HISTORY_KEY = "voice_history"
HOTKEY_STARTED_KEY = "hotkey_listener_started"

PAGE_STYLE = """
<style>
:root {
    color-scheme: dark;
    font-family: 'Inter', 'Segoe UI', sans-serif;
    background: #000000;
    overflow: hidden;
}
body {
    margin: 0 !important;
    background: #000000 !important;
}
section.main {
    padding: 0 !important;
    background: transparent !important;
}
#MainMenu, footer, header, .css-k1vhr4, .css-18e3th9, .css-1v0mbdj {
    display: none !important;
}
.stApp, .css-1d391kg {
    background: transparent !important;
}
.css-1d391kg {
    padding: 0 !important;
}
.block-container {
    padding-top: 10px !important;
    padding-left: 10px !important;
    padding-right: 10px !important;
    padding-bottom: 10px !important;
}
.stButton>button {
    border: 1px solid rgba(0,255,255,0.45) !important;
    background: rgba(0,15,30,0.88) !important;
    color: #e1ffff !important;
    border-radius: 18px !important;
    padding: 14px 22px !important;
    box-shadow: 0 0 28px rgba(0,255,255,0.18) !important;
}
.stButton>button:hover {
    background: rgba(0,255,255,0.12) !important;
}
</style>
"""

HEX_GRID_CSS = """
<style>
body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: radial-gradient(circle at 10% 10%, rgba(0,255,255,0.08), transparent 15%),
      linear-gradient(rgba(0,255,255,0.08) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,255,255,0.08) 1px, transparent 1px);
    background-size: 60px 60px, 30px 30px, 30px 30px;
    opacity: 0.35;
    pointer-events: none;
    z-index: -1;
}
</style>
"""

SPHERE_HTML = """
<style>
.neural-core-wrapper {
    width: 100%;
    min-height: 520px;
    padding: 20px;
    border-radius: 28px;
    background: rgba(1, 10, 25, 0.88);
    border: 1px solid rgba(0, 255, 255, 0.14);
    overflow: hidden;
}
.scene {
    position: relative;
    width: 100%;
    height: 460px;
    perspective: 900px;
}
.sphere {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 320px;
    height: 320px;
    transform-style: preserve-3d;
    transform: translate(-50%, -50%);
    animation: rotate 18s linear infinite;
}
.sphere .dot {
    position: absolute;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #00ffff;
    box-shadow: 0 0 20px rgba(0,255,255,0.95);
}
.sphere.red .dot {
    background: #ff1744;
    box-shadow: 0 0 26px rgba(255,23,68,0.96);
}
.status-ring {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 430px;
    height: 430px;
    margin-left: -215px;
    margin-top: -215px;
    border-radius: 50%;
    border: 2px solid rgba(0,255,255,0.12);
    box-shadow: 0 0 40px rgba(0,255,255,0.18);
    animation: pulse 2.8s infinite ease-in-out;
}
.sphere.red ~ .status-ring {
    border-color: rgba(255,23,68,0.28);
    box-shadow: 0 0 38px rgba(255,23,68,0.16);
}
@keyframes rotate {
    from { transform: translate(-50%, -50%) rotateX(0deg) rotateY(0deg); }
    to { transform: translate(-50%, -50%) rotateX(360deg) rotateY(360deg); }
}
@keyframes pulse {
    0%,100% { transform: scale(1); opacity: 0.85; }
    50% { transform: scale(1.02); opacity: 1; }
}
</style>
<div class="neural-core-wrapper">
    <div class="scene">
        <div class="sphere {status_class}">{dots}</div>
        <div class="status-ring"></div>
    </div>
</div>
"""

DIAL_CSS = """
<style>
.dial-card {
    width: 100%;
    min-height: 210px;
    padding: 20px;
    border-radius: 24px;
    background: rgba(4, 14, 32, 0.92);
    border: 1px solid rgba(0,255,255,0.14);
    box-shadow: inset 0 0 30px rgba(0,255,255,0.05);
    margin-bottom: 18px;
}
.dial-title {
    font-size: 16px;
    color: #8affff;
    margin-bottom: 12px;
}
.dial-ring {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    box-shadow: 0 0 24px rgba(0,255,255,0.12);
    margin: auto;
}
.dial-inner {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: #000000;
    display: grid;
    place-items: center;
    color: #d8f8ff;
    font-size: 24px;
    font-weight: 700;
}
</style>
"""

POWER_CSS = """
<style>
.power-card {
    border-radius: 24px;
    background: rgba(1, 12, 24, 0.88);
    border: 1px solid rgba(0,255,255,0.14);
    padding: 18px;
}
.power-card h4 {
    margin-bottom: 12px;
    color: #8affff;
}
.power-action {
    margin-bottom: 10px;
}
</style>
"""


def record_log(message: str):
    stamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
    entry = f"[{stamp}] [CORE STATE]: {message}"
    st.session_state[LOG_STATE_KEY].append(entry)
    if len(st.session_state[LOG_STATE_KEY]) > 100:
        st.session_state[LOG_STATE_KEY] = st.session_state[LOG_STATE_KEY][-100:]
    try:
        with open(LOG_DIR / "core.log", "a", encoding="utf-8") as handle:
            handle.write(entry + "\n")
    except Exception:
        pass


def init_state():
    st.set_page_config(page_title="ILLI OS v1.2.5", layout="wide", initial_sidebar_state="collapsed")
    defaults = {
        MIC_STATE_KEY: False,
        LOG_STATE_KEY: [],
        NET_STATE_KEY: [],
        NET_LAST_KEY: psutil.net_io_counters(),
        STATUS_MESSAGE_KEY: "Neural Matrix Synced.",
        WALLPAPER_PROFILE_KEY: "hex-grid",
        VOICE_HISTORY_KEY: [],
        HOTKEY_STARTED_KEY: False,
        "search_query": "",
        "wallpaper_path": "",
        "browser_url": "https://web.whatsapp.com",
        "scrape_url": "https://example.com",
        "scrape_selector": "body",
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

    if not st.session_state[HOTKEY_STARTED_KEY]:
        start_listener(on_hotkey_trigger)
        st.session_state[HOTKEY_STARTED_KEY] = True
        record_log("Global macro hotkey listener active.")


def on_hotkey_trigger():
    st.session_state["dashboard_hidden"] = not st.session_state.get("dashboard_hidden", False)
    record_log("Macro hotkey [Ctrl+Alt+I] received.")


def fetch_system_metrics():
    cpu = psutil.cpu_percent(interval=0.3)
    ram = psutil.virtual_memory().percent
    net = psutil.net_io_counters()
    prev = st.session_state[NET_LAST_KEY]
    download = max(0, net.bytes_recv - prev.bytes_recv) / 1024
    upload = max(0, net.bytes_sent - prev.bytes_sent) / 1024
    st.session_state[NET_LAST_KEY] = net
    st.session_state[NET_STATE_KEY].append({"download": round(download, 1), "upload": round(upload, 1)})
    if len(st.session_state[NET_STATE_KEY]) > 60:
        st.session_state[NET_STATE_KEY] = st.session_state[NET_STATE_KEY][-60:]
    return cpu, ram


def render_meter(label: str, value: float, hue: str) -> str:
    fill = int(value * 3.6)
    return f"""
    <div class='dial-card'>
        <div class='dial-title'>{label}</div>
        <div class='dial-ring' style='background: conic-gradient({hue} {fill}deg, rgba(255,255,255,0.08) {fill}deg 360deg);'>
            <div class='dial-inner'>{value:.0f}%</div>
        </div>
    </div>
    """


def build_sphere_html(active: bool) -> str:
    dots = "".join([
        f'<div class="dot" style="transform: rotateY({i * 18}deg) translateZ(170px);"></div>'
        for i in range(20)
    ])
    status_class = "red" if active else ""
    return SPHERE_HTML.replace("{status_class}", status_class).replace("{dots}", dots)


def calibrate_microphone(duration: float = 1.5) -> str:
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=duration)
            st.session_state["voice_ready"] = True
            st.session_state["threshold"] = recognizer.energy_threshold
            record_log("Ambient noise calibration complete.")
            return "Ambient noise profile set."
    except Exception as exc:
        record_log(f"Microphone calibration failed: {exc}")
        return f"Mic calibration failed: {exc}"


def listen_voice_command() -> str:
    recognizer = sr.Recognizer()
    if st.session_state.get("threshold"):
        recognizer.energy_threshold = st.session_state["threshold"]
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.8)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
            text = recognizer.recognize_sphinx(audio)
            st.session_state[VOICE_HISTORY_KEY].append(text)
            return parse_voice_command(text)
    except Exception as exc:
        record_log(f"Voice recognition failed: {exc}")
        return f"Voice error: {exc}"


def parse_voice_command(text: str) -> str:
    phrase = text.lower()
    record_log(f"Voice command captured: {text}")
    if "run system scan report" in phrase:
        report_path = BASE_DIR / "logs" / f"scan_report_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.txt"
        cpu, ram = fetch_system_metrics()
        with open(report_path, "w", encoding="utf-8") as out:
            out.write(f"CPU: {cpu:.1f}%\n")
            out.write(f"RAM: {ram:.1f}%\n")
            out.write(f"Report generated: {datetime.now(timezone.utc).isoformat()}\n")
        record_log(f"System scan report saved: {report_path.name}")
        return f"System scan report generated: {report_path.name}"
    if "shutdown" in phrase:
        shutdown()
        return "Shutdown sequence requested."
    if "restart" in phrase or "reboot" in phrase:
        restart()
        return "Restart sequence requested."
    if "sleep" in phrase or "suspend" in phrase:
        sleep()
        return "Sleep request sent."
    if "clear recycle" in phrase or "empty recycle" in phrase:
        clear_recycle_bin()
        return "Recycle bin cleared."
    if "launch" in phrase:
        target = phrase.replace("launch", "").strip()
        if target:
            if launch_local_application(target):
                return f"Launching local target: {target}"
    return f"Captured voice command: {text}"


def speak_message(message: str):
    try:
        engine = pyttsx3.init()
        engine.say(message)
        engine.runAndWait()
    except Exception:
        pass


def generate_wallpaper_profile(style: str = "hex-grid") -> str:
    wallpaper_path = BASE_DIR / "cache" / f"illi_wallpaper_{style}.png"
    wallpaper_path.parent.mkdir(parents=True, exist_ok=True)
    if style == "hex-grid":
        generate_hex_grid(str(wallpaper_path), size=1920, spacing=52, color=(0, 255, 255, 30))
    else:
        generate_hex_grid(str(wallpaper_path), size=1920, spacing=36, color=(255, 23, 68, 30))
    return str(wallpaper_path)


def apply_dynamic_wallpaper(style: str = "hex-grid") -> str:
    path = generate_wallpaper_profile(style)
    if set_wallpaper(path):
        record_log(f"Dynamic wallpaper applied: {style}")
        return f"Wallpaper applied from profile: {style}."
    return "Wallpaper application failed."


def search_local_files(query: str, max_results: int = 8):
    query = query.strip().lower()
    results = []
    if not query:
        return results
    roots = [Path(os.path.expanduser("~")), Path("C:/Program Files"), Path("C:/Program Files (x86)")]
    for root in roots:
        if not root.exists():
            continue
        for dirpath, _, filenames in os.walk(root):
            if len(results) >= max_results:
                break
            for filename in filenames:
                if query in filename.lower():
                    results.append(Path(dirpath) / filename)
                    if len(results) >= max_results:
                        break
        if len(results) >= max_results:
            break
    return results


def launch_local_application(target: str) -> bool:
    if not target:
        return False
    path = Path(target)
    if path.exists():
        try:
            os.startfile(str(path))
            record_log(f"Launched local application: {path}")
            return True
        except Exception as exc:
            record_log(f"Launch failed for {path}: {exc}")
            return False
    candidates = search_local_files(target, max_results=1)
    if candidates:
        return launch_local_application(str(candidates[0]))
    return False


def toggle_system_audio(mute: bool) -> str:
    if AudioUtilities is None or IAudioEndpointVolume is None:
        return "Audio automation is unavailable; install pycaw and comtypes."
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(1 if mute else 0, None)
        state = "muted" if mute else "unmuted"
        record_log(f"System audio {state}.")
        return f"System audio {state}."
    except Exception as exc:
        record_log(f"Audio toggle failed: {exc}")
        return f"Audio toggle failed: {exc}"


def open_whatsapp_gateway() -> str:
    if browser_agent is None:
        return "Browser automation module unavailable."
    try:
        browser_agent.open_whatsapp_persistent()
        return "WhatsApp gateway opened in local profile."
    except Exception as exc:
        return f"WhatsApp gateway error: {exc}"


def scrape_web_report(prompt: str, url: str, selector: str) -> str:
    if browser_agent is None:
        return "Browser automation module unavailable."
    try:
        browser_agent.scrape_to_markdown(prompt, url, selector)
        return "Browser report generated."
    except Exception as exc:
        return f"Browser scrape failed: {exc}"


def build_log_panel() -> str:
    rows = st.session_state[LOG_STATE_KEY][-35:]
    return "<div style='background:#01101c; border:1px solid rgba(0,255,255,0.12); border-radius:20px; padding:16px; min-height: 340px; max-height: 340px; overflow:auto; font-family: Consolas, monospace; font-size:13px; color:#c7f8ff;'>" + "<br>".join(rows) + "</div>"


def main():
    init_state()
    st.markdown(PAGE_STYLE + HEX_GRID_CSS, unsafe_allow_html=True)
    st.markdown(DIAL_CSS + POWER_CSS, unsafe_allow_html=True)

    if st.session_state.get("dashboard_hidden"):
        st.markdown("<div style='padding: 24px; color:#00ffff; font-size:28px;'>ILLI OS is sleeping. Press Ctrl+Alt+I to wake.</div>", unsafe_allow_html=True)
        return

    st.markdown("<div style='padding: 16px 0 12px 0; color:#7bf1ff; font-size:26px; font-weight:700;'>ILLI OS v1.2.5 - Principal Systems Engineer HUD</div>", unsafe_allow_html=True)

    left, center, right = st.columns([1, 2, 1], gap="large")
    cpu, ram = fetch_system_metrics()

    with left:
        st.markdown("<div style='padding:18px; border-radius:24px; background:rgba(1,12,26,0.92); border:1px solid rgba(0,255,255,0.14);'><h3 style='margin:0;color:#8affff;'>Hardware Telemetry HUD</h3></div>", unsafe_allow_html=True)
        st.markdown(render_meter("CPU Load", cpu, "#00ffff"), unsafe_allow_html=True)
        st.markdown(render_meter("RAM Utilization", ram, "#00ffff"), unsafe_allow_html=True)
        st.markdown("<div style='color:#b8f5ff; margin-top:12px;'>Live telemetry reflected each refresh cycle.</div>", unsafe_allow_html=True)

        st.markdown("<div class='power-card'><h4>System Power Overlord</h4></div>", unsafe_allow_html=True)
        if st.button("Sleep"):
            st.session_state[STATUS_MESSAGE_KEY] = "Sleep requested."
            sleep()
        if st.button("Restart"):
            st.session_state[STATUS_MESSAGE_KEY] = "Restart requested."
            restart()
        if st.button("Shutdown"):
            st.session_state[STATUS_MESSAGE_KEY] = "Shutdown requested."
            shutdown()
        if st.button("Clear Recycle Bin"):
            st.session_state[STATUS_MESSAGE_KEY] = "Recycle cleared." if clear_recycle_bin() else "Recycle clear failed."

        st.markdown("<div class='power-card'><h4>Audio Automation</h4></div>", unsafe_allow_html=True)
        if st.button("Mute System Audio"):
            st.session_state[STATUS_MESSAGE_KEY] = toggle_system_audio(True)
        if st.button("Unmute System Audio"):
            st.session_state[STATUS_MESSAGE_KEY] = toggle_system_audio(False)

    with center:
        st.markdown("<div style='padding:18px; border-radius:24px; background:rgba(1,12,26,0.92); border:1px solid rgba(0,255,255,0.14);'><h3 style='margin:0;color:#8cfffb;'>Neural Core & Voice Nexus</h3></div>", unsafe_allow_html=True)
        st.markdown(build_sphere_html(st.session_state[MIC_STATE_KEY]), unsafe_allow_html=True)

        voice_col1, voice_col2 = st.columns(2)
        with voice_col1:
            if st.button("Calibrate Mic"):
                st.session_state[STATUS_MESSAGE_KEY] = calibrate_microphone()
            if st.button("Listen Local Voice"):
                st.session_state[STATUS_MESSAGE_KEY] = listen_voice_command()
        with voice_col2:
            if st.button("Toggle Mic Reactive Core"):
                st.session_state[MIC_STATE_KEY] = not st.session_state[MIC_STATE_KEY]
                state = "active" if st.session_state[MIC_STATE_KEY] else "inactive"
                st.session_state[STATUS_MESSAGE_KEY] = f"Neural reactive mode {state}."
                record_log(st.session_state[STATUS_MESSAGE_KEY])
            if st.button("Speak Status"):
                speak_message(st.session_state[STATUS_MESSAGE_KEY] or "ILLI OS ready.")
                st.session_state[STATUS_MESSAGE_KEY] = "Spoken status to local speaker."

        st.markdown(f"<div style='color:#f6f6f6; margin-top: 12px; font-size:14px;'>Status: {st.session_state[STATUS_MESSAGE_KEY]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#8cfffb; margin-top: 8px; font-size:12px;'>Hotkey: Ctrl+Alt+I to toggle HUD visibility.</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div style='padding:18px; border-radius:24px; background:rgba(1,12,26,0.92); border:1px solid rgba(0,255,255,0.14);'><h3 style='margin:0;color:#8cfffb;'>Tactical Log Stream</h3></div>", unsafe_allow_html=True)
        st.markdown(build_log_panel(), unsafe_allow_html=True)
        st.line_chart(st.session_state[NET_STATE_KEY], height=240)

    st.markdown("---")
    st.markdown("<div style='padding:16px; border-radius:24px; background:rgba(1,12,26,0.92); border:1px solid rgba(0,255,255,0.14);'><h3 style='margin:0;color:#8affff;'>Advanced Local Search, Wallpaper & Gateway</h3></div>", unsafe_allow_html=True)

    query = st.text_input("Local Search or Launch Command", value=st.session_state["search_query"])
    wallpaper_path = st.text_input("Wallpaper image path (optional)", value=st.session_state["wallpaper_path"])
    browser_url = st.text_input("Browser gateway URL", value=st.session_state["browser_url"])
    scrape_url = st.text_input("Scrape URL", value=st.session_state["scrape_url"])
    scrape_selector = st.text_input("Scrape selector", value=st.session_state["scrape_selector"])

    st.session_state["search_query"] = query
    st.session_state["wallpaper_path"] = wallpaper_path
    st.session_state["browser_url"] = browser_url
    st.session_state["scrape_url"] = scrape_url
    st.session_state["scrape_selector"] = scrape_selector

    button_col1, button_col2, button_col3, button_col4 = st.columns(4)
    with button_col1:
        if st.button("Search Files"):
            st.session_state["last_search_results"] = [str(p) for p in search_local_files(query)]
            record_log(f"Local search executed for: {query}")
        if st.button("Launch Local App"):
            st.session_state[STATUS_MESSAGE_KEY] = "Launch requested." if launch_local_application(query) else "Launch failed."
    with button_col2:
        if st.button("Change Wallpaper"):
            if wallpaper_path:
                result = set_wallpaper(wallpaper_path)
                st.session_state[STATUS_MESSAGE_KEY] = "Wallpaper applied." if result else "Wallpaper failed."
            else:
                st.session_state[STATUS_MESSAGE_KEY] = apply_dynamic_wallpaper(st.session_state[WALLPAPER_PROFILE_KEY])
        if st.button("Generate Hex Wallpaper"):
            st.session_state[STATUS_MESSAGE_KEY] = apply_dynamic_wallpaper("hex-grid")
    with button_col3:
        if st.button("Open WhatsApp Gateway"):
            st.session_state[STATUS_MESSAGE_KEY] = open_whatsapp_gateway()
        if st.button("Scrape Web to Markdown"):
            st.session_state[STATUS_MESSAGE_KEY] = scrape_web_report(query or "Browser scrape", scrape_url, scrape_selector)
    with button_col4:
        if st.button("Create Diagnostic Snapshot"):
            snapshot = BASE_DIR / "logs" / f"diagnostic_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.txt"
            with open(snapshot, "w", encoding="utf-8") as handle:
                handle.write(f"CPU: {cpu:.1f}%\n")
                handle.write(f"RAM: {ram:.1f}%\n")
                handle.write(f"Network upload: {st.session_state[NET_STATE_KEY][-1]['upload'] if st.session_state[NET_STATE_KEY] else 0:.1f} KB\n")
                handle.write(f"Network download: {st.session_state[NET_STATE_KEY][-1]['download'] if st.session_state[NET_STATE_KEY] else 0:.1f} KB\n")
            record_log(f"Snapshot created: {snapshot.name}")
            try:
                os.startfile(snapshot)
            except Exception:
                pass
        if st.button("Apply Alt Wallpaper Profile"):
            st.session_state[STATUS_MESSAGE_KEY] = apply_dynamic_wallpaper("red-grid")

    if st.session_state.get("last_search_results"):
        st.markdown("<div style='margin-top:18px; color:#a8fff7; font-size:14px;'>Search Results:</div>", unsafe_allow_html=True)
        for result in st.session_state["last_search_results"]:
            st.markdown(f"<div style='color:#c7f8ff; font-size:13px;'>{result}</div>", unsafe_allow_html=True)

    if st.session_state[VOICE_HISTORY_KEY]:
        st.markdown("<div style='margin-top:18px; color:#8dffef; font-size:14px;'>Voice History:</div>", unsafe_allow_html=True)
        for item in st.session_state[VOICE_HISTORY_KEY][-5:]:
            st.markdown(f"<div style='color:#c7f8ff; font-size:13px;'>» {item}</div>", unsafe_allow_html=True)

    st.markdown("<script>setInterval(function(){try{window.dispatchEvent(new Event('streamlit:run'));}catch(e){window.location.reload();}}, 8000);</script>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
