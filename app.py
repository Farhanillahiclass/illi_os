"""
ILLI OS v1.2.5 - Main Application Wrapper
This module preserves the legacy app entrypoint while delegating to app_enhanced.py.
"""

from app_enhanced import init_session_state, render_main_hud

if __name__ == "__main__":
    init_session_state()
    render_main_hud()
