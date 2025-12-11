"""Run Desktop Application"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"

# Ensure src is on PYTHONPATH
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from jarvis.desktop.app import main

if __name__ == "__main__":
    main()
