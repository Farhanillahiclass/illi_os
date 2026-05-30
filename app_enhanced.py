"""
ILLI OS v1.2.5 - Enhanced HUD Application
Ghost-Protocol Matrix Interface with Multi-Agent Automation
"""

import streamlit as st
from illi_ai.interface import (
    inject_ghost_protocol_css,
    render_metric_dial,
    render_neural_core_canvas,
    render_threat_map,
    render_task_tracker,
    render_shell_stream,
    render_three_column_hud,
    initialize_hud_session_state,
    fetch_live_metrics,
    add_shell_log
)
from illi_ai.automation import (
    MasterAgentOrchestrator,
    SandboxBrowserAutomationEngine,
    DeepOSOverlordPowerManager,
    AutomationTask,
    TaskPriority
)
from illi_ai.core import (
    LocalMemorySystem,
    MultiVoiceSynthesisEngine,
    HandshakeDeleteProtection,
    AdaptiveMicrophoneCalibration
)
from pathlib import Path
import threading
import time
import re
import webbrowser
import subprocess
import ctypes
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus

# ============================================================================
# Page Configuration
# ============================================================================

st.set_page_config(
    page_title="ILLI OS - Ghost Protocol HUD",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# Session State Initialization
# ============================================================================

def init_session_state():
    """Initialize all session state variables"""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.agent_pool = None
        st.session_state.browser_engine = None
        st.session_state.memory_system = None
        st.session_state.voice_engine = None
        st.session_state.delete_protection = None
        st.session_state.mic_calibration = None
        st.session_state.power_manager = DeepOSOverlordPowerManager
        st.session_state.hotkey_thread = None
        st.session_state.hud_active = True
        st.session_state.active_tab = "Dashboard"
        st.session_state.tasks = []
        st.session_state.shell_logs = []
        st.session_state.url_history = []
        st.session_state.news_feed = []
        st.session_state.news_source = "Google News"
        st.session_state.status_message = "Ready"
        st.session_state.neural_status = "IDLE"
        st.session_state.is_listening = False
        
        # Initialize core systems
        initialize_hud_session_state()

def get_agent_pool():
    """Get or create master agent pool"""
    if st.session_state.agent_pool is None:
        st.session_state.agent_pool = MasterAgentOrchestrator(max_workers=4)
    return st.session_state.agent_pool

def get_memory():
    """Get or create memory system"""
    if st.session_state.memory_system is None:
        st.session_state.memory_system = LocalMemorySystem()
    return st.session_state.memory_system

def get_voice():
    """Get or create voice engine"""
    if st.session_state.voice_engine is None:
        st.session_state.voice_engine = MultiVoiceSynthesisEngine()
    return st.session_state.voice_engine

def get_deletion_protection(callback=None):
    """Get deletion protection handler"""
    if st.session_state.delete_protection is None:
        st.session_state.delete_protection = HandshakeDeleteProtection(confirmation_callback=callback)
    return st.session_state.delete_protection

def get_mic_cal():
    """Get microphone calibration"""
    if st.session_state.mic_calibration is None:
        st.session_state.mic_calibration = AdaptiveMicrophoneCalibration()
    return st.session_state.mic_calibration

# ============================================================================
# Business Logic Functions
# ============================================================================

def calibrate_microphone():
    """Calibrate microphone ambient noise"""
    st.session_state.status_message = "🎤 Calibrating microphone..."
    st.session_state.neural_status = "CALIBRATING"
    add_shell_log("Starting microphone calibration (3 seconds)...", "INFO")
    
    try:
        level = get_mic_cal().run_ambient_noise_check(3)
        st.session_state.status_message = f"✅ Calibration complete (Level: {level})"
        st.session_state.neural_status = "READY"
        add_shell_log(f"Microphone calibrated - Sensitivity: {level}", "SUCCESS")
    except Exception as e:
        st.session_state.status_message = f"❌ Calibration failed: {str(e)}"
        st.session_state.neural_status = "ERROR"
        add_shell_log(f"Calibration error: {str(e)}", "ERROR")

def listen_voice_command():
    """Listen for voice command"""
    st.session_state.is_listening = True
    st.session_state.status_message = "🎙️ Listening..."
    st.session_state.neural_status = "LISTENING"
    add_shell_log("Voice listener activated", "INFO")
    
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        
        calibration_level = get_mic_cal().get_calibration_sensitivity()
        if calibration_level:
            recognizer.energy_threshold = calibration_level * 100
        
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=10)

        command = None
        try:
            command = recognizer.recognize_sphinx(audio)
        except Exception as e_sphinx:
            add_shell_log(f"Sphinx unavailable or failed: {e_sphinx}", "WARNING")
            try:
                command = recognizer.recognize_google(audio)
            except Exception as e_google:
                raise RuntimeError(f"Speech recognition failed: {e_google}")

        if command:
            st.session_state.status_message = f"🗣️ Command: {command}"
            add_shell_log(f"Voice command recognized: {command}", "SUCCESS")
        else:
            raise RuntimeError("No voice command recognized")

        st.session_state.is_listening = False
        return command
    except Exception as e:
        st.session_state.status_message = f"❌ Voice error: {str(e)}"
        add_shell_log(f"Voice recognition error: {str(e)}", "ERROR")
        st.session_state.is_listening = False
        return None

def parse_voice_command(command: str):
    """Parse and execute voice command"""
    if not command:
        return
    
    cmd_lower = command.lower()
    
    if "shutdown" in cmd_lower:
        add_shell_log("SHUTDOWN COMMAND RECEIVED", "WARNING")
        st.session_state.power_manager.shutdown_system(delay_seconds=10)
    elif "restart" in cmd_lower:
        add_shell_log("RESTART COMMAND RECEIVED", "WARNING")
        st.session_state.power_manager.restart_system(delay_seconds=10)
    elif "sleep" in cmd_lower:
        add_shell_log("SLEEP COMMAND RECEIVED", "INFO")
        st.session_state.power_manager.sleep_system()
    elif "clear recycle" in cmd_lower or "empty trash" in cmd_lower:
        add_shell_log("CLEARING RECYCLE BIN", "INFO")
        st.session_state.power_manager.clear_recycle_bin()
        add_shell_log("Recycle bin cleared", "SUCCESS")
    elif "call me" in cmd_lower:
        new_name = command.lower().split("call me", 1)[-1].strip()
        if new_name:
            memory = get_memory()
            memory.set_preference("user_name", new_name)
            memory.update_voice_preference(new_name)
            add_shell_log(f"User name updated to '{new_name}'", "SUCCESS")
            get_voice().speak_adaptive(f"Acknowledged. I will call you {new_name}")
    elif "launch" in cmd_lower:
        app_name = cmd_lower.split("launch", 1)[-1].strip()
        add_shell_log(f"Launching: {app_name}", "INFO")
        st.session_state.power_manager.launch_application(app_name)
    elif "play video" in cmd_lower or "play youtube" in cmd_lower:
        query = command.lower()
        if "play video" in query:
            query = query.split("play video", 1)[-1].strip()
        elif "play youtube" in query:
            query = query.split("play youtube", 1)[-1].strip()
        if not query:
            query = "trending videos"
        add_shell_log(f"Playing video: {query}", "INFO")
        play_video_on_youtube(query)
    elif "open website" in cmd_lower or "browse to" in cmd_lower or "go to" in cmd_lower:
        query = command.lower()
        for phrase in ["open website", "browse to", "go to", "visit"]:
            if phrase in query:
                query = query.split(phrase, 1)[-1].strip()
                break
        if not query:
            query = "https://www.google.com"
        add_shell_log(f"Opening website: {query}", "INFO")
        open_website(query)
    elif "search for" in cmd_lower or "google" in cmd_lower or "web search" in cmd_lower:
        query = command.lower()
        if "search for" in query:
            query = query.split("search for", 1)[-1].strip()
        elif "google" in query:
            query = query.split("google", 1)[-1].strip()
        elif "web search" in query:
            query = query.split("web search", 1)[-1].strip()
        if not query:
            query = "latest news"
        add_shell_log(f"Searching web: {query}", "INFO")
        open_website(query)
    elif "mute" in cmd_lower and "audio" in cmd_lower:
        add_shell_log("Muting audio", "INFO")
        toggle_system_audio(True)
    elif "unmute" in cmd_lower and "audio" in cmd_lower:
        add_shell_log("Unmuting audio", "INFO")
        toggle_system_audio(False)
    elif "lock screen" in cmd_lower or "lock pc" in cmd_lower or "lock computer" in cmd_lower:
        add_shell_log("Locking screen", "INFO")
        lock_system()
    elif "scan" in cmd_lower or "report" in cmd_lower:
        add_shell_log("Running system scan...", "INFO")
        report = st.session_state.power_manager.run_system_scan_report()
        add_shell_log(report, "SUCCESS")

def speak_status():
    """Speak current status"""
    try:
        get_voice().select_voice("male")
        metrics = fetch_live_metrics()
        status_text = f"System status: CPU at {metrics['cpu']} percent, RAM at {metrics['ram']} percent. Neural core status is {st.session_state.neural_status}"
        get_voice().speak_adaptive(status_text)
        add_shell_log("Status spoken", "SUCCESS")
    except Exception as e:
        add_shell_log(f"TTS error: {str(e)}", "ERROR")

def search_files(query: str):
    """Search files in system"""
    try:
        import fnmatch
        import os

        results = []
        search_paths = [Path.cwd(), Path.home()]
        pattern = query.strip()
        if "*" not in pattern and "?" not in pattern:
            pattern = f"*{pattern}*"

        for root_path in search_paths:
            if not root_path.exists():
                continue
            try:
                for root, dirs, files in os.walk(root_path):
                    relative_depth = len(Path(root).relative_to(root_path).parts)
                    if relative_depth > 4:
                        continue
                    for file in files:
                        if fnmatch.fnmatch(file.lower(), pattern.lower()):
                            results.append(os.path.join(root, file))
                            if len(results) >= 20:
                                return results
            except Exception:
                continue

        return results[:20]
    except Exception as e:
        add_shell_log(f"Search error: {str(e)}", "ERROR")
        return []

def normalize_url(url: str) -> str:
    trimmed = url.strip()
    if not trimmed:
        return ""
    if trimmed.startswith("http://") or trimmed.startswith("https://"):
        return trimmed
    if re.match(r"^[\w\-]+\.[\w\.-]+", trimmed):
        return f"https://{trimmed}"
    return f"https://www.google.com/search?q={quote_plus(trimmed)}"


def add_url_history(url: str):
    target = normalize_url(url)
    if not target:
        return
    if "url_history" not in st.session_state:
        st.session_state.url_history = []
    if target in st.session_state.url_history:
        st.session_state.url_history.remove(target)
    st.session_state.url_history.insert(0, target)
    st.session_state.url_history = st.session_state.url_history[:20]


def get_url_history() -> list:
    return st.session_state.get("url_history", [])


def open_history_url(url: str) -> str:
    target = normalize_url(url)
    webbrowser.open_new_tab(target)
    add_shell_log(f"Opened history URL: {target}", "SUCCESS")
    add_url_history(target)
    return target


def fetch_live_news(source: str = "Google News") -> list:
    sources = {
        "Google News": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
        "BBC News": "http://feeds.bbci.co.uk/news/rss.xml",
        "Reuters": "https://www.reutersagency.com/feed/?best-topics=business"
    }
    feed_url = sources.get(source, sources["Google News"])
    try:
        response = requests.get(feed_url, timeout=8)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        items = root.findall('.//item') or root.findall('.//{http://www.w3.org/2005/Atom}entry')
        news_items = []
        for item in items[:12]:
            title = item.findtext('title') or item.findtext('{http://www.w3.org/2005/Atom}title', '')
            link = item.findtext('link') or item.findtext('{http://www.w3.org/2005/Atom}link', '')
            pub_date = item.findtext('pubDate') or item.findtext('{http://www.w3.org/2005/Atom}updated', '')
            if link is None and item.find('{http://www.w3.org/2005/Atom}link') is not None:
                link = item.find('{http://www.w3.org/2005/Atom}link').attrib.get('href', '')
            news_items.append({
                "title": title.strip() if title else "Untitled",
                "link": link.strip() if link else "",
                "pubDate": pub_date.strip() if pub_date else ""
            })
        return news_items
    except Exception as e:
        add_shell_log(f"News fetch failed: {str(e)}", "ERROR")
        return []


def open_website(url: str) -> str:
    target = normalize_url(url)
    add_url_history(target)
    webbrowser.open_new_tab(target)
    add_shell_log(f"Opened website: {target}", "SUCCESS")
    return target


def play_video_on_youtube(query: str) -> str:
    trimmed = query.strip()
    if not trimmed:
        trimmed = "trending videos"
    if "youtube.com/watch" in trimmed or "youtu.be" in trimmed:
        target = trimmed if trimmed.startswith("http") else f"https://{trimmed}"
    else:
        target = f"https://www.youtube.com/results?search_query={quote_plus(trimmed)}"
    add_url_history(target)
    webbrowser.open_new_tab(target)
    add_shell_log(f"Playing YouTube: {target}", "SUCCESS")
    return target


def lock_system() -> bool:
    try:
        ctypes.windll.user32.LockWorkStation()
        add_shell_log("Screen lock invoked", "INFO")
        return True
    except Exception as e:
        add_shell_log(f"Lock screen failed: {str(e)}", "ERROR")
        return False


def toggle_system_audio(mute: bool = True) -> bool:
    try:
        success = st.session_state.power_manager.toggle_audio_mute(mute=mute)
        if success:
            add_shell_log(f"Audio {'muted' if mute else 'unmuted'}", "SUCCESS")
        else:
            add_shell_log("Audio control unavailable", "WARNING")
        return success
    except Exception as e:
        add_shell_log(f"Audio toggle failed: {str(e)}", "ERROR")
        return False


def open_task_manager() -> bool:
    try:
        subprocess.Popen(["taskmgr"])
        add_shell_log("Task Manager opened", "SUCCESS")
        return True
    except Exception as e:
        add_shell_log(f"Task Manager failed: {str(e)}", "ERROR")
        return False


def launch_app(app_name: str):
    """Launch application"""
    try:
        add_shell_log(f"Launching: {app_name}", "INFO")
        st.session_state.power_manager.launch_application(app_name)
        add_shell_log(f"{app_name} launched successfully", "SUCCESS")
    except Exception as e:
        add_shell_log(f"Launch error: {str(e)}", "ERROR")


def on_hotkey_trigger():
    """Hotkey callback - toggle HUD visibility"""
    st.session_state.hud_active = not st.session_state.hud_active
    add_shell_log(f"HUD toggled: {'ON' if st.session_state.hud_active else 'OFF'}", "INFO")

def start_hotkey_listener():
    """Start global hotkey listener - Note: Hotkeys work on desktop, not in web browser"""
    try:
        from illi_ai import hotkeys
        if st.session_state.hotkey_thread is None or not st.session_state.hotkey_thread.is_alive():
            st.session_state.hotkey_thread = threading.Thread(
                target=hotkeys.start_listener,
                args=(on_hotkey_trigger,),
                daemon=True
            )
            st.session_state.hotkey_thread.start()
            add_shell_log("Hotkey listener started (Ctrl+Alt+I to toggle)", "SUCCESS")
    except Exception as e:
        add_shell_log(f"Hotkey setup: {str(e)}", "WARNING")

# ============================================================================
# Main HUD Render
# ============================================================================

def render_main_hud():
    """Render main Ghost-Protocol HUD"""
    
    # Inject custom CSS
    inject_ghost_protocol_css()
    
    # Title with glow effect
    st.markdown(
        '<h1 style="text-align: center; color: #00ffff; text-shadow: 0 0 20px #00ffff;">⚙️ ILLI OS v1.2.5</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p style="text-align: center; color: #00cc99; font-size: 12px;">Ghost-Protocol HUD Matrix | Local AI Agent</p>',
        unsafe_allow_html=True
    )
    
    # Start hotkey listener
    start_hotkey_listener()
    
    # Fetch live metrics
    metrics = fetch_live_metrics()
    
    # Update display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("CPU", f"{metrics['cpu']}%", delta="System")
    with col2:
        st.metric("RAM", f"{metrics['ram']}%", delta="Memory")
    with col3:
        st.metric("Status", st.session_state.status_message, delta=st.session_state.neural_status)
    with col4:
        st.metric("Logs", len(st.session_state.shell_logs), delta="Entries")
    
    st.divider()
    
    page_tabs = st.tabs(["Dashboard", "Web Automation", "Live News"])

    with page_tabs[0]:
        left_col, center_col, right_col = st.columns([1, 2, 1])
        
        # ====== LEFT COLUMN: METRICS ======
        with left_col:
            st.markdown("### 📊 METRICS")
            st.markdown(
                render_metric_dial("CPU", metrics['cpu'], 100, "%"),
                unsafe_allow_html=True
            )
            st.markdown(
                render_metric_dial("RAM", metrics['ram'], 100, "%"),
                unsafe_allow_html=True
            )
        
        # ====== CENTER COLUMN: NEURAL CORE & CONTROLS ======
        with center_col:
            st.markdown("### 🧠 NEURAL CORE")
            st.markdown(
                render_neural_core_canvas(st.session_state.is_listening, st.session_state.neural_status),
                unsafe_allow_html=True
            )
            st.divider()
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🎤 Calibrate Mic", use_container_width=True):
                    calibrate_microphone()
                    st.rerun()
            with col2:
                if st.button("🎙️ Listen", use_container_width=True):
                    command = listen_voice_command()
                    if command:
                        parse_voice_command(command)
                    st.rerun()
            with col3:
                if st.button("📢 Speak Status", use_container_width=True):
                    speak_status()
                    st.rerun()
        
        # ====== RIGHT COLUMN: THREATS & TASKS ======
        with right_col:
            st.markdown("### 📋 ACTIVITY")
            tabs = st.tabs(["Threats", "Tasks", "Log"])
            with tabs[0]:
                st.markdown(render_threat_map(), unsafe_allow_html=True)
            with tabs[1]:
                st.markdown(render_task_tracker(st.session_state.tasks), unsafe_allow_html=True)
            with tabs[2]:
                st.markdown(render_shell_stream(st.session_state.shell_logs, max_entries=10), unsafe_allow_html=True)

        st.divider()
        
        st.markdown("### ⚡ POWER MANAGEMENT")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("💤 Sleep", use_container_width=True):
                add_shell_log("SLEEP command executed", "WARNING")
                st.session_state.power_manager.sleep_system()
        with col2:
            if st.button("🔄 Restart", use_container_width=True):
                add_shell_log("RESTART command executed - 10 second delay", "WARNING")
                st.session_state.power_manager.restart_system(delay_seconds=10)
        with col3:
            if st.button("⛔ Shutdown", use_container_width=True):
                add_shell_log("SHUTDOWN command executed - 10 second delay", "WARNING")
                st.session_state.power_manager.shutdown_system(delay_seconds=10)
        with col4:
            if st.button("🗑️ Clear Recycle", use_container_width=True):
                add_shell_log("Clearing recycle bin...", "INFO")
                st.session_state.power_manager.clear_recycle_bin()
                add_shell_log("Recycle bin cleared", "SUCCESS")
                st.rerun()

        st.divider()
        
        st.markdown("### 🚀 LAUNCH APPLICATIONS")
        col1, col2 = st.columns(2)
        with col1:
            app_name = st.text_input("App to launch:", placeholder="e.g., notepad, calculator, chrome")
            if st.button("🔗 Launch App", use_container_width=True):
                if app_name:
                    launch_app(app_name)
                    st.rerun()
        with col2:
            search_query = st.text_input("Search files:", placeholder="e.g., *.txt, document")
            if st.button("🔍 Search", use_container_width=True):
                if search_query:
                    results = search_files(search_query)
                    add_shell_log(f"Found {len(results)} files matching '{search_query}'", "SUCCESS")
                    st.rerun()

    with page_tabs[1]:
        st.markdown("### 🌐 Web Automation")
        st.markdown("Use URL history and quick web actions to control browsing from ILLI.")
        url_input = st.text_input("URL or search query:", placeholder="e.g., youtube.com, openai.com, search cats")
        video_query = st.text_input("YouTube search or direct URL:", placeholder="e.g., relax music video")
        action_col1, action_col2, action_col3 = st.columns(3)
        with action_col1:
            if st.button("🌐 Open Website", use_container_width=True):
                if url_input:
                    open_website(url_input)
                    st.rerun()
        with action_col2:
            if st.button("▶️ Play Video", use_container_width=True):
                if video_query:
                    play_video_on_youtube(video_query)
                    st.rerun()
        with action_col3:
            if st.button("🔎 Search Web", use_container_width=True):
                if url_input:
                    open_website(url_input)
                    st.rerun()

        st.divider()
        st.markdown("### 🔁 URL History")
        history = get_url_history()
        if history:
            for idx, item in enumerate(history):
                row_col1, row_col2 = st.columns([5, 1])
                row_col1.markdown(f"{idx + 1}. [{item}]({item})")
                if row_col2.button("Open", key=f"history_open_{idx}"):
                    open_history_url(item)
                    st.rerun()
        else:
            st.info("URL history is empty. Open a website to begin tracking.")

        if st.button("🗑️ Clear URL History", use_container_width=True):
            st.session_state.url_history = []
            st.rerun()

        st.divider()
        st.markdown("### ⚡ Quick Browser Actions")
        quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
        with quick_col1:
            if st.button("🔇 Mute Audio", use_container_width=True):
                toggle_system_audio(True)
                st.rerun()
        with quick_col2:
            if st.button("🔊 Unmute Audio", use_container_width=True):
                toggle_system_audio(False)
                st.rerun()
        with quick_col3:
            if st.button("🔒 Lock Screen", use_container_width=True):
                lock_system()
                st.rerun()
        with quick_col4:
            if st.button("🧠 Task Manager", use_container_width=True):
                open_task_manager()
                st.rerun()

    with page_tabs[2]:
        st.markdown("### 📰 Live News Feed")
        st.markdown("Fetch real-time headlines from public news feeds and browse stories directly.")
        source = st.selectbox("News Source:", ["Google News", "BBC News", "Reuters"], index=["Google News", "BBC News", "Reuters"].index(st.session_state.news_source) if st.session_state.news_source in ["Google News", "BBC News", "Reuters"] else 0)
        st.session_state.news_source = source
        if st.button("🔄 Refresh News", use_container_width=True):
            st.session_state.news_feed = fetch_live_news(source)
        if not st.session_state.news_feed:
            st.info("No news loaded yet. Click Refresh News to load headlines.")
        else:
            for item in st.session_state.news_feed:
                link = item.get("link", "")
                title = item.get("title", "Untitled")
                pub_date = item.get("pubDate", "")
                if link:
                    st.markdown(f"- [{title}]({link})  \n*{pub_date}*")
                else:
                    st.markdown(f"- {title}  \n*{pub_date}*")

    st.divider()
    
    # ====== SHELL LOG ======
    st.markdown("### 📡 SHELL STREAM")
    st.markdown(render_shell_stream(st.session_state.shell_logs, max_entries=20), unsafe_allow_html=True)
    
    # Sidebar info
    with st.sidebar:
        st.markdown("### 📖 ILLI OS INFO")
        st.markdown("""
        **Version:** 1.2.5  
        **Type:** Local AI Agent  
        **Mode:** Ghost-Protocol HUD  
        **Status:** 🟢 Active
        """)
        
        st.divider()
        
        memory = get_memory()
        prefs = memory.get_preference("user_name", "User")
        st.markdown(f"**User:** {prefs}")
        
        st.divider()
        
        if st.button("Refresh Metrics"):
            st.rerun()

# ============================================================================
# Main Execution
# ============================================================================

if __name__ == "__main__":
    init_session_state()
    render_main_hud()
