"""
ILLI OS v1.2.5 - Unified Launcher
This module launches the full HUD when available, with a fallback to the enhanced HUD.
"""

import importlib
import streamlit as st


def run_app():
    """Try app_full first, then fallback to app_enhanced."""
    try:
        app_full = importlib.import_module("app_full")
        if hasattr(app_full, "main"):
            app_full.main()
            return
    except Exception as exc:
        st.warning(f"Unable to launch full HUD from app_full.py: {exc}")

    try:
        from app_enhanced import init_session_state, render_main_hud
        init_session_state()
        render_main_hud()
    except Exception as exc:
        st.error(f"Unable to launch enhanced HUD from app_enhanced.py: {exc}")


if __name__ == "__main__":
    run_app()
