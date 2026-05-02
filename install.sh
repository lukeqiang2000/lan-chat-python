#!/bin/bash

echo "========================================"
echo "  LAN Chat System - Dependency Installer"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed!"
    echo ""
    echo "Please install Python 3 from: https://www.python.org/downloads/"
    echo "Or use Homebrew: brew install python3"
    exit 1
fi

echo "[OK] Python 3 is installed"
python3 --version
echo ""

# Check if pip is available
if ! python3 -m pip --version &> /dev/null; then
    echo "[ERROR] pip is not available!"
    echo ""
    echo "Please install pip:"
    echo "  python3 -m ensurepip --upgrade"
    echo "  OR"
    echo "  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py"
    echo "  python3 get-pip.py"
    exit 1
fi

echo "[OK] pip is available"
python3 -m pip --version
echo ""

# Upgrade pip
echo "[1/3] Upgrading pip..."
python3 -m pip install --upgrade pip
echo ""

# Install dependencies
echo "[2/3] Installing dependencies..."
echo "Installing PyQt5..."
python3 -m pip install PyQt5
echo "Installing PyInstaller..."
python3 -m pip install pyinstaller
echo ""

# Verify installation
echo "[3/3] Verifying installation..."
python3 -c "import PyQt5; print('  PyQt5: OK')" 2>/dev/null || echo "  PyQt5: FAILED"
python3 -c "import PyInstaller; print('  PyInstaller: OK')" 2>/dev/null || echo "  PyInstaller: FAILED"
echo ""

echo "========================================"
echo "  Installation Complete!"
echo "========================================"
echo ""
echo "You can now run:"
echo "  - Server: python3 chat_server.py"
echo "  - Client: python3 chat_gui.py"
echo ""
