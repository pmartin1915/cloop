@echo off
REM Ultrathink - Safe Launcher with Auto-Cleanup
REM Automatically stops old instances and starts fresh

echo.
echo ========================================
echo    Ultrathink Safe Launcher
echo ========================================
echo.

cd /d "%~dp0"

REM Step 1: Stop any existing Streamlit instances
echo [1/3] Checking for existing instances...
taskkill /F /IM streamlit.exe 2>nul
if errorlevel 1 (
    echo No existing instances found.
) else (
    echo Stopped existing instances.
    timeout /t 2 /nobreak >nul
)

REM Step 2: Find available port
echo.
echo [2/3] Finding available port...
set PORT=8501
for /L %%p in (8501,1,8510) do (
    netstat -ano | findstr ":%%p " >nul
    if errorlevel 1 (
        set PORT=%%p
        goto :found_port
    )
)

:found_port
echo Found available port: %PORT%

REM Step 3: Launch dashboard
echo.
echo [3/3] Starting Ultrathink Dashboard...
echo Opening in your browser at http://localhost:%PORT%
echo.
echo Press Ctrl+C to stop the server
echo.

poetry run streamlit run ui\Home.py --server.port %PORT%

pause
