@echo off
echo Setting up Ultrathink for VSCode...
echo.

REM Copy tasks to workspace
if not exist ".vscode" mkdir .vscode
copy /Y .vscode\tasks.json .vscode\tasks.json >nul

echo [OK] VSCode tasks installed
echo.
echo Quick Start:
echo 1. Open any Python file in VSCode
echo 2. Press Ctrl+Shift+P
echo 3. Type "Run Task"
echo 4. Select "Ultrathink: Quick Handoff"
echo 5. Copy ultrathink_handoff.md and paste into Amazon Q!
echo.
echo Or press Ctrl+Shift+B for quick access!
echo.
pause
