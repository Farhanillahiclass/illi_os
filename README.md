# ILLI OS README

ILLI OS v1.2.5

Local, offline AI desktop agent and automation HUD.

Quick start:

1) Create a virtualenv and install requirements:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Run Streamlit HUD:

```powershell
streamlit run app.py
```

3) Or use CLI:

```powershell
pip install -e .
illi-ai --launch
```

Security: This project is fully local and requires no external API keys.
