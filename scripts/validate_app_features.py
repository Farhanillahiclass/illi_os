import os
import streamlit as st
import webbrowser
from app_enhanced import normalize_url, add_url_history, get_url_history, get_trending_hashtags, fetch_live_news, play_video_on_youtube
from illi_ai.automation import DeepOSOverlordPowerManager

os.chdir("c:/Users/Muhammad Anas/f_illi")

# Prepare minimal session state
if hasattr(st, 'session_state'):
    st.session_state.clear()
    st.session_state.url_history = []

# Override browser open to avoid opening tabs during test
webbrowser.open_new_tab = lambda url: True

print('normalize_url:', normalize_url('example.com'))
print('search_normalize:', normalize_url('openai chatgpt'))
add_url_history('example.com')
add_url_history('https://www.google.com')
print('history', get_url_history())
print('yt', play_video_on_youtube('test video query'))
print('tags', get_trending_hashtags([{'title': 'OpenAI releases GPT-5 Beta and AI news update'}]))
news = fetch_live_news('BBC News')
print('news count', len(news))
print('news first', news[0] if news else 'none')
pm = DeepOSOverlordPowerManager()
report = pm.run_system_scan_report()
print('scan len', len(report))
