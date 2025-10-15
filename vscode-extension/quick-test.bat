@echo off
echo ========================================
echo Ultrathink Extension Quick Test
echo ========================================
echo.

echo [1/4] Testing Ultrathink CLI...
cd ..\
poetry run ultrathink --help >nul 2>&1
if %errorlevel% neq 0 (
    echo FAIL: Ultrathink CLI not working
    exit /b 1
)
echo PASS: Ultrathink CLI working

echo.
echo [2/4] Installing extension dependencies...
cd vscode-extension
call npm install >nul 2>&1
if %errorlevel% neq 0 (
    echo FAIL: npm install failed
    exit /b 1
)
echo PASS: Dependencies installed

echo.
echo [3/4] Compiling TypeScript...
call npm run compile >nul 2>&1
if %errorlevel% neq 0 (
    echo FAIL: TypeScript compilation failed
    exit /b 1
)
echo PASS: Compilation successful

echo.
echo [4/4] Testing Ultrathink analyze...
cd ..
poetry run ultrathink analyze --path vscode-extension\test-file.py --no-save-findings
if %errorlevel% neq 0 (
    echo FAIL: Analysis failed
    exit /b 1
)
echo PASS: Analysis working

echo.
echo ========================================
echo All tests passed!
echo ========================================
echo.
echo Next steps:
echo 1. Open vscode-extension folder in VS Code
echo 2. Press F5 to launch Extension Development Host
echo 3. Open test-file.py
echo 4. Right-click and select "Ultrathink: Analyze Current File"
echo.
pause
