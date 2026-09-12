@echo off
chcp 65001 > nul
title తెలుగు డైలీ కరెంట్ అఫైర్స్ - విండోస్ ఆటోమేటిక్ షెడ్యూలర్ సెటప్

echo ====================================================================
echo   రోజూ ఉదయం 7:00 AM కు ఆటోమేటిక్ అప్‌డేట్స్ కోసం విండోస్ టాస్క్ సెటప్
echo ====================================================================
echo.

set PYTHON_CMD=python
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
)

set SCRIPT_PATH=%~dp0scheduler.py

echo [1/2] Windows Task Scheduler లో 'TeluguDailyCurrentAffairs' టాస్క్ నమోదు చేయబడుతోంది...
schtasks /create /tn "TeluguDailyCurrentAffairs" /tr "\"%PYTHON_CMD%\" \"%SCRIPT_PATH%\"" /sc daily /st 07:00 /f

if %ERRORLEVEL% equ 0 (
    echo.
    echo ✅ విజయం! రోజూ ఉదయం 07:00 AM కు ఆటోమేటిక్ అప్‌డేట్స్ టాస్క్ షెడ్యూల్ చేయబడింది.
    echo వార్తలు ఆటోమేటిక్‌గా ఫెచ్ అయి మీ టెలిగ్రామ్‌కు చేరతాయి.
) else (
    echo.
    echo ⚠️ టాస్క్ క్రియేట్ చేయడానికి అడ్మినిస్ట్రేటర్ అనుమతి అవసరం కావచ్చు.
    echo దయచేసి ఈ ఫైల్‌ను 'Run as administrator' ద్వారా రన్ చేయండి.
)

echo.
pause
