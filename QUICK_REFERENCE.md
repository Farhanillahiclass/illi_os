# ⚡ ILLI OS - Quick Reference

## 🚀 Launch (One Command)
```powershell
cd c:\Users\Muhammad Anas\f_illi
.\.venv\Scripts\python.exe -m streamlit run app_full.py
```

**Then open:** http://localhost:8501

---

## 🎯 Main Features (One Sentence Each)

| Feature | How To |
|---------|--------|
| **System Status** | Dashboard tab - see CPU, RAM, metrics |
| **Sleep/Restart/Shutdown** | Power tab - click buttons |
| **Calibrate Microphone** | Voice tab → "Calibrate Mic" |
| **Change Voice** | Voice tab → Select voice → "Set Voice" |
| **Speak Status Aloud** | Voice tab → "Speak Status" |
| **Launch Apps** | Launcher tab → type app name → Launch |
| **Find Files** | Files tab → type pattern (*.txt) → Search |
| **Full System Report** | Diagnostics tab → "Full System Report" |
| **Save Your Name** | Preferences tab → type name → "Save Name" |
| **Set Wallpaper** | Preferences tab → "Generate Hex Grid" or "Red Grid" |

---

## 🎤 Voice Commands (When Implemented)

```
"shutdown"              → Power down in 10 seconds
"restart"               → Restart in 10 seconds
"sleep"                 → Sleep now
"clear recycle"         → Empty recycle bin
"launch [app]"          → Launch application
"call me [name]"        → Save your preferred name
"system report"         → Generate diagnostics
```

---

## 📊 Keyboard Shortcuts (Desktop App Only)

| Keys | Action |
|------|--------|
| **Ctrl+Alt+I** | Toggle HUD visibility |
| **F5** | Refresh browser |

---

## 💾 Your Data Location

```
~/.illi_memory/cognition.db        ← Your preferences, history, calibration
cache/hex_grid.png                 ← Generated wallpaper
cache/red_grid.png                 ← Alternative wallpaper
```

---

## 🆘 Quick Troubleshooting

**App won't start?**
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Microphone issues?**
```powershell
# Open Windows sound settings
mmsys.cpl
```

**Port already in use?**
```powershell
# Use different port
streamlit run app_full.py --server.port 8502
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app_full.py` | Main HUD (use this!) |
| `app_enhanced.py` | Alternative enhanced UI |
| `app.py` | Simple wrapper |
| `requirements.txt` | Dependencies |
| `setup.py` | Package configuration |

---

## 🔥 Pro Tips

1. **Calibrate first:** Do Voice tab → "Calibrate Mic" before using voice
2. **Set your name:** Preferences tab → Save your name → Voice will use it
3. **Check logs:** All activity logged in Shell Stream at bottom
4. **Use patterns:** File search → `*.txt` finds all text files
5. **App names:** Works with: `notepad`, `calculator`, `chrome`, `vscode`, etc.

---

## ✅ Checklist (First Time)

- [ ] Launched app at http://localhost:8501
- [ ] Saw system metrics on dashboard
- [ ] Went to Voice tab
- [ ] Clicked "Calibrate Mic"
- [ ] Set preferred voice
- [ ] Tested "Speak Status" 
- [ ] Went to Launcher tab
- [ ] Launched an app (e.g., notepad)
- [ ] Set your name in Preferences
- [ ] Clicked "Generate Hex Grid" wallpaper

---

## 🎉 You're Ready!

Explore the tabs, try the features, and enjoy your personal AI assistant!

For detailed feature documentation, see **FEATURES_COMPLETE.md**
