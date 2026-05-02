@echo off
echo ========================================
echo   LAN Chat System - Dependency Installer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Check if pip is available
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip is not available!
    echo.
    echo Please reinstall Python with pip included.
    pause
    exit /b 1
)

echo [OK] pip is available
echo.

REM Upgrade pip
echo [1/3] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo [2/3] Installing dependencies...
echo Installing PyQt5...
python -m pip install PyQt5
echo Installing PyInstaller...
python -m pip install pyinstaller
echo.

REM Verify installation
echo [3/3] Verifying installation...
python -c "import PyQt5; print('  PyQt5: OK')" 2>nul || echo   PyQt5: FAILED
python -c "import PyInstaller; print('  PyInstaller: OK')" 2>nul || echo   PyInstaller: FAILED
echo.

echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo You can now run:
echo   - Server: python chat_server.py
echo   - Client: python chat_gui.py
echo.
pause
