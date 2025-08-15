@echo off
echo 🚀 Quick Git Push
echo.
if "%~1"=="" (
    python quick_push.py
) else (
    python quick_push.py %*
)
echo.
echo ✅ Done! Check your GitHub repository.
pause
