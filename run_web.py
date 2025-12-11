"""Run Web Application"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"

# Ensure src is on PYTHONPATH
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from jarvis.config.settings import FLASK_DEBUG, FLASK_HOST, FLASK_PORT
from jarvis.web.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT)
