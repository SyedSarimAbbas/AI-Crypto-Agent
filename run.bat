@echo off
setlocal
echo ==========================================
echo    AI Crypto Agent - 3D Experience
echo ==========================================
echo.

echo [1/3] Checking Dependencies...
pip install fastapi uvicorn pydantic requests > nul 2>&1

echo [2/3] Starting Backend Server...
REM Kill any existing process on port 8000 to avoid conflicts
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /f /pid %%a > nul 2>&1
)

start /b python backend/main_api.py

echo [3/3] Opening 3D Dashboard...
timeout /t 5 /nobreak > nul
start http://localhost:8000

echo.
echo Launch Successful! 
echo.
echo [IMPORTANT] Please close any browser tabs from 
echo             other projects (like Pizza Palace) 
echo             to avoid connection conflicts.
echo.
echo Keep this window open while using the agent.
echo.
pause
