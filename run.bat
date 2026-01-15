@echo off
echo Starting Crypto Agent Environment...

REM Check if virtual environment exists (optional check, assuming user has env active or global)
REM In a full setup, we might create venv here. For now, just install requirements and run.

echo Installing/Verifying Dependencies...
pip install requests streamlit > nul 2>&1

echo Launching Streamlit App...
streamlit run app.py

pause
