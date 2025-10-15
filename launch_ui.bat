@echo off
echo.
echo ========================================
echo   Ultrathink Dashboard
echo   Starting web interface...
echo ========================================
echo.

cd /d "%~dp0"

REM Clear cache for fresh start
echo Clearing cache...
rmdir /S /Q .streamlit 2>nul
del /S /Q ui\__pycache__ 2>nul
del /S /Q ui\pages\__pycache__ 2>nul

echo Launching UI...
echo.
poetry run ultrathink ui

if errorlevel 1 (
    echo.
    echo ========================================
    echo   Failed to start dashboard
    echo   Check the error message above
    echo ========================================
)

pause
