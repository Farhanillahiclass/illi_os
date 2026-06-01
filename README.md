# 🖥️ ILLI: The Autonomous Local AI Operating System

**Local. Offline. Autonomous.**

My name is Muhammad Farhan. I am a student of artificial intelligence and currently doing an internship at MRS (Muslim Review Skills).

ILLI is designed to be your personal AI Engineer, Dev Assistant, and Realtime Copilot, providing a Jarvis-like experience entirely on your local machine.

---

## ⚡ Quick Start (5 minutes)

### Prerequisites
- Windows 10/11
- Python 3.10+
- Git (for version control)

### Installation

```powershell
# Clone or navigate to project
cd path\to\f_illi

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Install package with CLI entry point (optional)
pip install -e .
```

### Launch HUD

**Method 1: Direct Streamlit (Recommended - Full Features)**
```powershell
.\.venv\Scripts\python.exe -m streamlit run app_full.py
```

**Method 2: Direct Streamlit (Enhanced HUD)**
```powershell
.\.venv\Scripts\python.exe -m streamlit run app_enhanced.py
```

**Method 3: Unified Launcher (Recommended)**
```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```
This entrypoint attempts to launch `app_full.py` first and falls back to `app_enhanced.py` if the full HUD cannot load.

**Method 4: CLI Entry Point** (requires `pip install -e .`)
```powershell
illi-ai --launch
```

**Assistant Dispatch Script**
```powershell
python scripts\assistant_dispatcher.py --command "open chrome"
python scripts\assistant_dispatcher.py --scan-apps
python scripts\assistant_dispatcher.py --list-apps
```

Access the HUD at: **http://localhost:8501**

This project is licensed under the MIT License. See `LICENSE` for details.

---

## 🎨 Features

### Part 1: Ghost-Protocol HUD Matrix Interface

**Pitch-black cyberpunk interface** with neon-cyan (#00ffff) procedural hex-grid background.

#### Three-Column Asymmetric Layout:

**LEFT PANEL - Hardware Telemetry HUD**
- Real-time CPU Load animated dial
- Memory (RAM) monitoring system
- Thermal & Load metrics for systems engineers

**CENTER PANEL - Active Agent Matrix**
- Real-time AI agent status and feedback
- Contextual information display
- Interactive command processing

**RIGHT PANEL - Terminal & Network**
- Active terminal sessions
- Network activity monitoring
- System event logs

---

## 🤝 Contributing

Contributions welcome! Follow this workflow:

1. Create feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Commit with clear messages:
   ```bash
   git commit -m "Add: Description of feature"
   ```

3. Push and create Pull Request:
   ```bash
   git push origin feature/your-feature-name
   ```

---

## 📜 License

ILLI OS v1.2.5 is released under the MIT License. See LICENSE file for details.

---

## 👨‍💻 Author

**Muhammad Farhan** - Core Windows Kernel Developer & Cyberpunk UI Architect

Designed and built for Principal Systems Engineers who demand:
- Zero compromise on privacy
- Maximum control and automation
- Cutting-edge cyberpunk aesthetics
- Local-first architecture

---

## 🔗 Links

- **GitHub**: https://github.com/Farhanillahiclass/illi_os
- **Issues**: https://github.com/Farhanillahiclass/illi_os/issues
- **Discussions**: https://github.com/Farhanillahiclass/illi_os/discussions

---

**ILLI OS: Where AI meets absolute local autonomy.** 🌐✨