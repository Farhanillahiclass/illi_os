"""
Centralized Logging Utility for ILLI OS.
Handles shell stream logs and file logging.
"""
import streamlit as st
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents # illi/utils -> illi -> project_root
LOG_FILE_PATH = BASE_DIR / "logs" / "illi_core.log"
LOG_FILE_PATH.parent.mkdir(exist_ok=True, parents=True)

def add_shell_log(message: str, level: str = "INFO"):
    """Add entry to Streamlit shell stream log and file log."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry_text = f"[{timestamp}] [{level}]: {message}"
    
    if "shell_logs" not in st.session_state:
        st.session_state["shell_logs"] = []
    st.session_state["shell_logs"].append({"timestamp": timestamp, "level": level, "message": message})
    if len(st.session_state["shell_logs"]) > 50: # Keep last 50 entries in session state
        st.session_state["shell_logs"] = st.session_state["shell_logs"][-50:]
    
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(entry_text + "\n")