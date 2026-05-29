# Minimal setup script for ILLI OS HUD
# Run this from the repository root folder.

Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Push-Location $projectRoot

Write-Host "Removing existing .venv if it exists..."
if (Test-Path .venv) {
    Remove-Item .venv -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "Creating virtual environment..."
python -m venv .venv

Write-Host "Upgrading pip, setuptools, and wheel..."
.\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel -q

Write-Host "Installing minimal runtime dependencies..."
.\.venv\Scripts\python.exe -m pip install streamlit psutil pynput pyttsx3 pillow python-dotenv requests --default-timeout=100 -q

Write-Host "Minimal setup complete. Launch the HUD with:"
Write-Host "  .\.venv\Scripts\python.exe -m streamlit run app.py"

Pop-Location
