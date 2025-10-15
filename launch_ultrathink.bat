@echo off
REM Ultrathink - One-Click Launcher with Smart Port Detection
REM Opens the beautiful dashboard in your browser

echo.
echo ========================================
echo    Starting Ultrathink Dashboard...
echo ========================================
echo.

cd /d "%~dp0"

REM Try ports 8501-8510 until we find an available one
for /L %%p in (8501,1,8510) do (
    netstat -ano | findstr ":%%p " >nul
    if errorlevel 1 (
        echo Found available port: %%p
        echo Opening in your browser at http://localhost:%%p
        echo.
        echo Press Ctrl+C to stop the server
        echo.
        poetry run streamlit run ui\Home.py --server.port %%p
        goto :end
    ) else (
        echo Port %%p is busy, trying next...
    )
)

echo.
echo ERROR: All ports 8501-8510 are in use!
echo Please close other Streamlit instances or manually specify a port:
echo poetry run streamlit run ui\Home.py --server.port 8520
echo.

:end
pause
