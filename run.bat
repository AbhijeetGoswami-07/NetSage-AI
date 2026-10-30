@echo off
title NetSage AI - Running
cd /d "%~dp0"

echo ===================================================
echo               NetSage AI Launcher
echo ===================================================
echo.

if not exist ".venv\Scripts\streamlit.exe" (
    echo [ERROR] Virtual environment not found.
    echo Setting up environment...
    python -m venv .venv
    .venv\Scripts\pip install -r requirements.txt
)

echo Starting NetSage AI Streamlit application...
echo The app will automatically open in your default web browser.
echo URL: http://localhost:8501
echo.

".venv\Scripts\streamlit.exe" run app.py

pause
