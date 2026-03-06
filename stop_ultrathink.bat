@echo off
REM Stop all running Streamlit instances

echo.
echo ========================================
echo    Stopping Ultrathink Dashboard...
echo ========================================
echo.

REM Kill all streamlit processes
taskkill /F /IM streamlit.exe 2>nul
if errorlevel 1 (
    echo No Streamlit processes found running.
) else (
    echo Successfully stopped all Streamlit instances.
)

REM Also try killing Python processes running streamlit
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr "PID:"') do (
    netstat -ano | findstr ":850" | findstr "%%a" >nul
    if not errorlevel 1 (
        taskkill /F /PID %%a 2>nul
        echo Stopped Python process %%a
    )
)

echo.
echo All Streamlit instances stopped.
echo You can now run launch_ultrathink.bat again.
echo.

pause
