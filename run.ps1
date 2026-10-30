Set-Location $PSScriptRoot

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "               NetSage AI Launcher" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path ".venv\Scripts\streamlit.exe")) {
    Write-Host "Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv .venv
    .\.venv\Scripts\pip install -r requirements.txt
}

Write-Host "Starting NetSage AI Streamlit application..." -ForegroundColor Green
Write-Host "URL: http://localhost:8501" -ForegroundColor Yellow
Write-Host ""

& .\.venv\Scripts\streamlit.exe run app.py
