@echo off
echo ========================================
echo   GutCheck - Build and Run
echo ========================================
echo.

echo [1/4] Installing Python dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    exit /b 1
)
echo Done!
echo.

echo [2/4] Installing Node.js dependencies...
cd gutcheck-web
call npm install --legacy-peer-deps
if errorlevel 1 (
    echo ERROR: Failed to install Node.js dependencies
    exit /b 1
)
echo Done!
echo.

echo [3/4] Building React frontend...
call npm run build
if errorlevel 1 (
    echo ERROR: Failed to build frontend
    exit /b 1
)
echo Done!
echo.

echo [4/4] Starting FastAPI server...
cd ..
echo.
echo ========================================
echo   GutCheck is running!
echo   Open: http://localhost:7860
echo ========================================
echo.
python gutcheck-web\main.py
