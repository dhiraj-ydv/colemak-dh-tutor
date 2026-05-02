@echo off
setlocal
set RESTART_FILE=restart.trigger
set STOP_FILE=stop.trigger

:loop
if exist %RESTART_FILE% del %RESTART_FILE%
if exist %STOP_FILE% del %STOP_FILE%

cls
echo ==========================================
echo    Colemak-DH Touch Typing Tutor
echo ==========================================
echo.
echo Starting processes...

:: Launch Backend and Frontend in minimized windows
start "Colemak_Backend" /min cmd /c ".\backend\venv\Scripts\activate && python run.py"
start "Colemak_Frontend" /min cmd /c "cd frontend && npm run dev"

echo.
echo App is now running!
echo ------------------------------------------
echo Frontend: http://localhost:5175
echo Backend:  http://localhost:5000
echo ------------------------------------------
echo.
echo Keep this window open to manage the app.
echo Use the "Stop App" button in the menu to exit.
echo.

:monitor
:: Check for triggers every 2 seconds
timeout /t 2 > nul
if exist %STOP_FILE% (
    echo [System] Stop signal received. Cleaning up...
    del %STOP_FILE%
    echo [System] App stopped successfully.
    pause
    exit
)
if exist %RESTART_FILE% (
    echo [System] Restart signal received. Re-launching...
    timeout /t 2 > nul
    goto loop
)
goto monitor
