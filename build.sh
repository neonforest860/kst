#!/bin/bash

# Exit on error
set -e

echo "Starting build process..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Build with PyInstaller
echo "Building application..."
pyinstaller --clean --windowed main.py --name "KonectTrafficStudio" \
    --add-data "assets:assets" \
    --add-data "utils:utils" \
    --add-data "components:components" \
    --hidden-import PyQt6.QtPrintSupport \
    --hidden-import PyQt6.QtSvg \
    --hidden-import PyQt6.QtWebEngineCore \
    --hidden-import PyQt6.QtWebEngineWidgets \
    --hidden-import PyQt6.QtWebEngine \
    --hidden-import PyQt6.QtWebEngineQuick \
    --hidden-import PyQt6.QtNetwork \
    --hidden-import PyQt6.QtWebChannel

# Create installer with Inno Setup
echo "Creating Windows installer..."
mkdir -p installer
WINEPREFIX="/home/ngra/.wine_inno" wine "/home/ngra/.wine_inno/drive_c/Program Files (x86)/Inno Setup 6/ISCC.exe" "Z:$(pwd)/KonectTrafficStudio.iss"

echo "Build process completed!"