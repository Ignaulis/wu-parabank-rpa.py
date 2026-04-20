#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "[1/5] Creating virtual environment..."
python3 -m venv venv

echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo "[3/5] Upgrading pip..."
python -m pip install --upgrade pip

echo "[4/5] Installing requirements..."
pip install -r requirements.txt

echo "[5/5] Installing Playwright browsers..."
playwright install

echo
echo "Setup completed successfully."
echo "You can now run: ./run_mac.command"
