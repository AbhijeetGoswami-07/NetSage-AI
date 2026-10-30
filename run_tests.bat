@echo off
title NetSage AI - Tests
cd /d "%~dp0"

echo ===================================================
echo               NetSage AI Test Suite
echo ===================================================
echo.

".venv\Scripts\pytest.exe" -v

echo.
pause
