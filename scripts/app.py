"""
ILLI OS - Main Application Orchestrator
Ghost-Protocol HUD + Advanced Automation Engine + Local Cognition
"""

import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
import streamlit as st

# ILLI AI Modular Components
from illi.ui.interface import (
    inject_ghost_protocol_css,
    render_metric_dial,
    render_neural_core_canvas,
    render_threat_map,
    render_task_tracker,
    render_shell_stream,
    initialize_hud_session_state,
    fetch_live_metrics,
    render_three_column_hud,
    render_whiteboard_hub
)
from illi.automation.master_agent import get_master_agent
from illi.automation.power_manager import DeepOSOverlordPowerManager
from illi.brain.core import get_memory_system, get_voice_engine, get_mic_calibration
from illi.automation.hotkeys import start_listener
from illi.automation.power_manager import clear_recycle_bin, restart, shutdown, sleep
from illi.ui.wallpaper import generate_hex_grid, set_wallpaper
from illi.utils.logger import add_shell_log

BASE_DIR = Path(__file__).resolve().parent

def init_system():
    """Initialize session state and core background workers"""
    initialize_hud_session_state()
    
    if "hotkey_listener" not in st.session_state:
        def hotkey_callback():
            st.session_state["hud_active"] = not st.session_state.get("hud_active", True)
            add_shell_log("Global Hotkey [Ctrl+Alt+I] triggered.", "CORE")
            
        start_listener(hotkey_callback)
        st.session_state["hotkey_listener"] = True
        add_shell_log("Background Hotkey Hooks synchronized.", "SUCCESS")

    # Initialize Sub-Agent Pool
    if "agent" not in st.session_state:
        st.session_state["agent"] = get_master_agent( # This will be refactored to illi.agents.master_agent
            callback=lambda e: add_shell_log(f"Agent: {e.get('name')} {e.get('type')}", "CORE")
        )

def on_hotkey_trigger():
    st.session_state["hud_active"] = not st.session_state.get("hud_active", True)

def main():
    st.set_page_config(page_title="ILLI OS v1.2.5", layout="wide", initial_sidebar_state="collapsed")
    init_system()
    inject_ghost_protocol_css()

    if not st.session_state.get("hud_active", True):
        st.markdown("<div style='background:#000; height:100vh; display:grid; place-items:center; color:#0ff; font-size:2em;'>ILLI OS SECURE SLEEP. Press Ctrl+Alt+I.</div>", unsafe_allow_html=True)
        return

    # Telemetry
    metrics = fetch_live_metrics()
    
    # Handle Tab Logic
    if "active_tab" not in st.session_state:
        st.session_state["active_tab"] = "threat_hub"

    # 3-Column Layout
    left_col = f"""
        {render_metric_dial('CPU LOAD', metrics['cpu'])}
        {render_metric_dial('RAM USAGE', metrics['ram'])}
        <div style="margin-top: 20px; font-size: 0.8em; color: rgba(0, 255, 255, 0.6);">
            NETWORK_IO:<br>
            TX: {metrics.get('net_bytes_sent', 0) / 1024 / 1024:.2f} MB<br>
            RX: {metrics.get('net_bytes_recv', 0) / 1024 / 1024:.2f} MB
        </div>
    """
    
    neural_status = st.session_state.get('neural_status', 'ACTIVE')
    mic_active = st.session_state.get('mic_listening', False)
    
    center_col = f"""
        {render_neural_core_canvas(is_listening=mic_active, status=neural_status)}
        <div style="margin-top: 10px; text-align: center; color: {'#ff3333' if mic_active else '#00ffff'};">
            {f"[ LISTENING ]" if mic_active else f"[ SYSTEM {neural_status} ]"}
        </div>
    """
    
    # Modular Tabs on Right
    active_tab = st.session_state["active_tab"]
    tab_content = ""
    if active_tab == "threat_hub":
        tab_content = render_threat_map()
    elif active_tab == "whiteboard":
        tab_content = render_whiteboard_hub()
    elif active_tab == "tasks":
        tab_content = render_task_tracker(st.session_state.get('tasks', []))

    right_col = f"""
        <div class="tab-container" style="display: flex; gap: 5px; margin-bottom: 10px;">
            <div class="tab-button {'active' if active_tab == 'threat_hub' else ''}" style="padding: 5px; font-size: 0.7em;">INTEL</div>
            <div class="tab-button {'active' if active_tab == 'whiteboard' else ''}" style="padding: 5px; font-size: 0.7em;">FLOW</div>
            <div class="tab-button {'active' if active_tab == 'tasks' else ''}" style="padding: 5px; font-size: 0.7em;">TASKS</div>
        </div>
        <div class="tab-content">
            {tab_content}
        </div>
        <div style="margin-top: 10px;">
            {render_shell_stream(st.session_state.get('shell_logs', []), max_entries=5)}
        </div>
    """
    
    render_three_column_hud(left_col, center_col, right_col)

    # Interactive Control Matrix
    st.markdown("<div style='margin-top: -30px;'></div>", unsafe_allow_html=True)
    
    # Row 1: Tab Control & Voice
    r1c1, r1c2, r1c3, r1c4 = st.columns(4)
    with r1c1:
        if st.button("INTEL HUB", use_container_width=True):
            st.session_state["active_tab"] = "threat_hub"
            st.rerun()
    with r1c2:
        if st.button("FLOWCHART", use_container_width=True):
            st.session_state["active_tab"] = "whiteboard"
            st.rerun()
    with r1c3:
        if st.button("TASK LIST", use_container_width=True):
            st.session_state["active_tab"] = "tasks"
            st.rerun()
    with r1c4:
        if st.button("🎤 LISTEN", use_container_width=True):
            st.session_state["mic_listening"] = True
            add_shell_log("Voice recognition sub-agent activated.", "CORE")
            st.rerun()

    # Row 2: Automation & System
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🎤 Sync Acoustics"):
            cal = get_mic_calibration()
            level = cal.run_ambient_noise_check()
            add_shell_log(f"Calibration complete: {level:.1f}% threshold set.", "SUCCESS")
            st.rerun()
    with c2:
        search_q = st.text_input("Launcher", placeholder="e.g. chrome", label_visibility="collapsed")
        if st.button("🚀 EXECUTE", use_container_width=True):
            if search_q: # This will be refactored to illi.automation.app_launcher
                DeepOSOverlordPowerManager.launch_application(search_q)
                add_shell_log(f"Application booter initiated: {search_q}", "CORE")
    with c3:
        if st.button("🖼️ Rotate Grid"):
            path = generate_hex_grid(str(BASE_DIR / "cache" / "grid.png"))
            set_wallpaper(path)
            add_shell_log("Hexagonal lattice wallpaper synchronized.", "SUCCESS")
    with c4:
        if st.button("🛑 System Shutdown"):
            add_shell_log("SHUTDOWN SEQUENCE AUTHORIZED.", "WARNING")
            shutdown()

    # Bottom Log Display
    st.markdown(render_shell_stream(st.session_state.get('shell_logs', []), max_entries=10), unsafe_allow_html=True)

    # Auto-reload script for live telemetry
    st.markdown("<script>setInterval(function(){try{window.dispatchEvent(new Event('streamlit:run'));}catch(e){}}, 4000);</script>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
