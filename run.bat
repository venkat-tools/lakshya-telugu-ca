@echo off
chcp 65001 > nul
title తెలుగు డైలీ కరెంట్ అఫైర్స్ డ్యాష్‌బోర్డ్ (Daily Current Affairs)

echo ====================================================================
echo   తెలుగు పోటీ పరీక్షల డైలీ కరెంట్ అఫైర్స్ డ్యాష్‌బోర్డ్
echo   APPSC / TSPSC / UPSC / SSC / Banking Special
echo ====================================================================
echo.

set PYTHON_CMD=python
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
)

echo [1/2] సర్వర్ ప్రారంభమవుతోంది...
start "" "%PYTHON_CMD%" backend\app.py

timeout /t 2 /nobreak > nul

echo [2/2] మీ డిఫాల్ట్ బ్రౌజర్‌లో వెబ్‌సైట్ ఓపెన్ చేయబడుతోంది...
start http://localhost:5000

echo.
echo అప్లికేషన్ విజయవంతంగా రన్ అవుతోంది! (http://localhost:5000)
echo సర్వర్ ఆపివేయడానికి ఈ విండోను మూసివేయండి.
echo.
pause
