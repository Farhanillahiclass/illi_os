# 🎯 ILLI OS v1.2.5 - Complete Feature Guide

## Launch Options

| Command | Features | Use Case |
|---------|----------|----------|
| `streamlit run app_full.py` | **🌟 ALL FEATURES** | Full-featured HUD with all controls |
| `streamlit run app_enhanced.py` | Enhanced layout | Alternative enhanced interface |
| `streamlit run app.py` | Basic wrapper | Simple lightweight launcher |

**Recommended:** Use `app_full.py` for the complete experience.

---

## 🎯 Dashboard Tab
- **System Metrics**: Real-time CPU, RAM, Network I/O
- **Neural Core Visualization**: 3D rotating wireframe (toggles color when listening)
- **Activity Tracking**: Threat map, task tracker, log viewer
- **Status Indicators**: System status, neural core state

---

## ⚡ Power Management Tab

### Power Control
- **💤 Sleep System** - Puts system to sleep immediately
- **🔄 Restart** - Restarts after 10-second delay (cancellable)
- **⛔ Shutdown** - Shuts down after 10-second delay (cancellable)
- **🗑️ Clear Recycle Bin** - Permanently empties Windows Recycle Bin

---

## 🎤 Voice & Audio Control Tab

### Microphone Management
- **🎙️ Calibrate Mic** - 3-second ambient noise baseline calibration
  - Stores calibration level in local memory
  - Auto-applies to speech recognition
  
### Voice Selection
- **Voice Type**: Male or Female (pyttsx3 offline voices)
- **Set Voice**: Apply selected voice for all TTS operations

### Audio Output
- **📢 Speak Status** - Current system status read aloud
  - Includes user's preferred name
  - Reports CPU %, RAM %, Neural core status

---

## 🚀 Application Launcher Tab

### Launch Any App
- Type application name: `notepad`, `calculator`, `chrome`, `vscode`, `spotify`, etc.
- Searches PATH and launches application
- Supports full file paths too
- Logs success/failure to shell stream

**Examples:**
```
notepad              → Opens Notepad
calculator           → Opens Windows Calculator
chrome               → Opens Chrome browser
vscode               → Opens Visual Studio Code
C:\path\to\app.exe   → Launches specific application
```

---

## 🔍 File Search Tab

### Find Files with Patterns
- **Search Patterns**: `*.txt`, `*.py`, `document*`, `*.log`
- **Automatic Wildcard**: `report` → searches `*report*`
- **Depth Limit**: Restricts search to 3-4 levels deep (prevents hangs)
- **Results**: Shows up to 15 matching files
- **Paths**: Searches current directory and home folder

**Examples:**
```
*.txt                → Find all text files
*.py                 → Find all Python files
config*              → Find files starting with "config"
*backup*             → Find files containing "backup"
```

---

## 📊 System Diagnostics Tab

### Hardware Information
- **🔧 Full System Report**
  - CPU count, usage percentage
  - Total/available/used RAM in GB
  - Percentage of memory in use
  - Disk space for all drives (C:, D:, E:, etc.)
  - System boot time
  - Exports as JSON

- **💾 Memory Status**
  - Total RAM percentage
  - Available RAM in GB
  - Visual indicator

- **🌡️ CPU Status**
  - Current CPU usage percentage
  - Real-time measurement

---

## 👤 Preferences & Memory Tab

### User Preferences
- **Call Me**: Set your preferred name
  - Stored in SQLite database
  - Used by TTS voice synthesis
  - Persistent across restarts
  - Example: "Call me Alice" → system says "Hello Alice"

- **View Preferences**: Display current saved preferences

### Wallpaper Control
- **🔷 Generate Hex Grid**
  - Creates cyan neon hex pattern
  - Applies as Windows desktop wallpaper
  - Cyberpunk aesthetic

- **🔴 Generate Red Grid**
  - Creates red dot pattern
  - Alternative cyberpunk aesthetic
  - Applies as Windows desktop wallpaper

---

## 📡 Shell Stream (Bottom of All Pages)

### Real-Time Activity Log
- **Timestamps**: Synchronized local time for all events
- **Log Levels**: 
  - `[SUCCESS]` (green) - Operation completed
  - `[ERROR]` (red) - Operation failed
  - `[WARNING]` (orange) - Important notification
  - `[INFO]` (cyan) - General information
  - `[CORE]` (cyan) - Core system event

- **Entries**: Shows last 20 entries by default
- **Clearing**: Use "Clear Logs" button in sidebar

**Example Logs:**
```
[23:18:27] [SUCCESS]: ILLI OS v1.2.5 initialized
[23:18:28] [INFO]: Microphone calibration started
[23:18:31] [SUCCESS]: Mic calibrated - Sensitivity: 45.2
[23:19:00] [INFO]: Launching: notepad
[23:19:01] [SUCCESS]: Launched: notepad
```

---

## 🧠 Memory & Persistence

### Local SQLite Database
**Location:** `~/.illi_memory/cognition.db`

### Stored Data
- **User Preferences**: Custom names, voice preferences
- **Mic Calibration**: Ambient noise levels, environment type
- **Interaction History**: Past voice commands, responses
- **Voice Profiles**: Male/female voice settings

### Features
- ✅ Survives app restarts
- ✅ Thread-safe operations
- ✅ JSON serialization for complex types
- ✅ Timestamped entries

---

## 🔧 System Integration

### Global Hotkey (Desktop Only)
- **Ctrl+Alt+I** - Toggle HUD visibility (when running as desktop app)
- Works on Windows desktop
- Does NOT work in web browser (Streamlit limitation)

### Windows APIs Used
- **Power Control**: `rundll32`, `shutdown` command
- **Recycle Bin**: `SHEmptyRecycleBin` COM interface
- **Wallpaper**: `SystemParametersInfoW` Win32 API
- **Audio**: `pycaw` / `pycoreutils` for volume control
- **Microphone**: `SpeechRecognition` library
- **TTS**: `pyttsx3` offline synthesizer

---

## 🔐 Safety Features

### Deletion Protection Handshake
- Before destructive operations: requires voice/text confirmation
- "HANDSHAKE" prompt with target filename
- Must respond "YES", "Y", "CONFIRM", or "PROCEED"
- Prevents accidental data loss

### Graceful Degradation
- Missing dependencies don't crash the app
- Features fail safely with error messages
- Always shows operational status

---

## 💡 Usage Tips

### Optimal Setup
1. Run `.\scripts\setup_minimal.ps1` for quick install
2. Launch with `streamlit run app_full.py`
3. Calibrate microphone before using voice features
4. Set your preferred name in Preferences tab

### Workflow Example
```
1. Launch app_full.py
2. Calibrate microphone (Mic & Audio tab)
3. Set preference name (Preferences tab)
4. Use voice commands or GUI buttons
5. Monitor activity in Shell Stream
```

### Performance Tips
- Minimize "Full System Report" usage (CPU intensive)
- File searches work best with specific patterns
- Voice recognition works better after microphone calibration
- Keep Shell Stream history under 50 entries for UI performance

---

## 🐛 Troubleshooting

### "Import failed: speech_recognition"
**Solution:** Install SpeechRecognition
```powershell
.\.venv\Scripts\pip.exe install SpeechRecognition pyttsx3
```

### Microphone not detected
**Solution:** Ensure microphone is plugged in and enabled in Windows
```powershell
# Check audio devices:
mmsys.cpl  # Opens Sound settings
```

### Wallpaper won't apply
**Solution:** Ensure file path is valid and writable
```powershell
mkdir cache  # Create cache directory if missing
```

### Streamlit won't start
**Solution:** Check if port 8501 is already in use
```powershell
# Use different port:
streamlit run app_full.py --server.port 8502
```

---

## 📦 Requirements

### Minimal Install (app runs with core features)
```
streamlit
psutil
pynput
pyttsx3
Pillow
python-dotenv
requests
```

### Full Install (all optional features)
```
# Add automation:
pip install -e ".[automation,visual,data]"
```

---

## 📝 Examples

### Example 1: Daily System Check
```
1. Launch HUD
2. Go to "Diagnostics" tab
3. Click "Full System Report"
4. View CPU, RAM, disk usage
5. Check in Shell Stream for status
```

### Example 2: Setting User Name
```
1. Go to "Preferences" tab
2. Type your name in "Call me:" field
3. Click "Save Name"
4. Go to "Voice" tab
5. Click "Speak Status" - will use your name!
```

### Example 3: Quick App Launch
```
1. Go to "Launcher" tab
2. Type "chrome"
3. Click "Launch"
4. Chrome opens automatically
5. Status logged in Shell Stream
```

### Example 4: Searching Files
```
1. Go to "Files" tab
2. Type "*.txt"
3. Click "Search"
4. Results shown in expandable section
5. Copy path or open manually
```

---

## 🎨 Customization

### Change Theme Colors
Edit `GHOST_PROTOCOL_CSS` in `illi_ai/interface.py`:
- `#00ffff` → Cyan (primary)
- `#00cc99` → Teal (secondary)
- `#000000` → Black (background)

### Add Custom Features
1. Create function in `app_full.py`
2. Add new tab in main tab layout
3. Use `add_shell_log()` for status updates
4. Restart app

---

## ✅ Verification Checklist

- [ ] Streamlit running at localhost:8501
- [ ] Dashboard shows system metrics
- [ ] Microphone calibration works
- [ ] TTS speaks status
- [ ] App launcher opens applications
- [ ] File search finds files
- [ ] System diagnostics display
- [ ] Preferences save and persist
- [ ] Shell Stream logs events
- [ ] Wallpaper applies successfully

---

**Happy automating! 🤖**
