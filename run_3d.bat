@echo off
echo Starting AI Crypto Agent 3D Experience...
echo.
echo 1. Launching FastAPI Backend...
REM Kill any existing process on port 8000 to avoid conflicts
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /f /pid %%a > nul 2>&1
)
start /b python backend/main_api.py
echo.
echo 2. Waiting for server to initialize...
timeout /t 5 > nul
echo.
echo 3. Opening 3D Dashboard...
start http://localhost:8000
echo.
echo Done! Please minimize this window.
pause
