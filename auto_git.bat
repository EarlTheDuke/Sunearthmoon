@echo off
echo 🌍 Sun-Earth-Moon Simulation - Auto Git Operations
echo ==================================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python first.
    pause
    exit /b 1
)

REM Run the auto git script
python auto_git.py

echo.
echo ✅ Auto Git operations completed!
echo.
echo To run the simulation:
echo python sun_earth_moon_simulation.py
echo.
pause
