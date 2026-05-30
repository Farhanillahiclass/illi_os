# ILLI Wiki

This repository wiki provides user-facing documentation, feature references, and troubleshooting notes for the ILLI local AI operating system.

## Overview

ILLI is an offline-capable AI operating system for Windows that blends voice control, real-time HUD telemetry, browser automation, and system-level functions.

## Key Sections

- **Quick Start**: Setup environment, install dependencies, launch the app.
- **HUD Features**: Detailed descriptions of dashboard panels, voice controls, and automation tabs.
- **Live News**: Real-time RSS feeds, trending topic filters, and hashtag jump buttons.
- **Web Automation**: Open websites, play videos, search YouTube, and manage URL history.
- **System Controls**: Audio mute toggle, lock screen, Task Manager launch, shutdown/reboot controls.
- **Troubleshooting**: Common issues and fixes.

## Quick Start

### Prerequisites
- Windows 10/11
- Python 3.10+
- Git

### Installation

```powershell
cd path\to\f_illi
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

### Launch HUD

```powershell
.\.venv\Scripts\python.exe -m streamlit run app_full.py
```

For the enhanced HUD:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app_enhanced.py
```

## HUD Sections

### Dashboard
- CPU and RAM telemetry
- System status logs
- Voice mode indicators

### Web Automation Tab
- Open websites from a quick-entry list
- URL history tracking
- YouTube search and playback support

### Live News Tab
- Choose from Google News, BBC News, or Reuters
- Refresh live RSS headlines
- Scrollable news ticker for top stories
- Trending topic filters and hashtag sidebar for instant topic jumps

### System Controls
- Mute/unmute Windows audio
- Lock the screen
- Open Task Manager
- Clear the recycle bin and manage shutdown actions

## New Live News Features

### Trending Hashtag Sidebar
- Headlines are scanned for hashtags and keywords
- Click any displayed hashtag to refresh news with that topic
- Supports quick navigation to trending discussion points

### News Ticker
- Shows the first 5 headlines in a scrolling ticker bar
- Keeps the HUD updated with breaking stories

## Troubleshooting

### Streamlit warnings
A harmless `missing ScriptRunContext` warning may appear when importing Streamlit outside the normal runtime. It can be ignored when running the app normally with `streamlit run`.

### If the app fails to load
- Confirm the virtual environment is activated
- Confirm dependencies are installed from `requirements.txt`
- Run `python -m py_compile app_enhanced.py` to check for syntax errors

## Contribution Notes

This wiki file is part of the repository and can be expanded with further technical details, screenshots, or deployment instructions.

For live GitHub wiki pages, this document can be used as the initial source content.
