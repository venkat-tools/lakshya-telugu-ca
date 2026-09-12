@echo off
chcp 65001 > nul
title తెలుగు కరెంట్ అఫైర్స్ - టెలిగ్రామ్ బోట్ (Telegram Bot)

echo ====================================================================
echo   తెలుగు పోటీ పరీక్షల కరెంట్ అఫైర్స్ - టెలిగ్రామ్ బోట్ సర్వీస్
echo ====================================================================
echo.

set PYTHON_CMD=python
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
)

echo బోట్ ప్రారంభమవుతోంది...
"%PYTHON_CMD%" backend\run_bot.py

pause
