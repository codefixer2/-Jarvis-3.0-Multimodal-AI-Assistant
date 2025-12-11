# JARVIS 3.0 - Project Structure

All source now lives under the `jarvis` package inside `src/`, with web assets bundled under the package for a single source of truth.

## 📁 Directory Structure

```
JARVIS3.0/
├── app.py                  # Web entry wrapper -> jarvis.web.app
├── run_web.py              # Launch Flask app (adds ./src to PYTHONPATH)
├── run_desktop.py          # Launch Tkinter desktop app (adds ./src)
├── requirements.txt
├── README.md
├── PROJECT_STRUCTURE.md    # This file
├── src/
│   └── jarvis/
│       ├── __init__.py
│       ├── api/            # API + Gemini integration
│       ├── config/         # Settings + env loading
│       ├── desktop/        # Desktop UI + controllers
│       ├── utils/          # Shared helpers
│       └── web/            # Flask web app + assets
│           ├── app.py
│           ├── templates/  # index.html
│           └── static/     # css/, js/
└── tests/
    └── __init__.py
```

## 🚀 Running the Applications

On Windows (cmd):
```bash
set PYTHONPATH=%cd%\src
python run_web.py
python run_desktop.py
```

CLI API interface:
```bash
set PYTHONPATH=%cd%\src
python -m jarvis.api.cli
```

## 📦 Module Highlights

- `jarvis.web`: Flask app factory + bundled `templates/` and `static/`
- `jarvis.api`: Gemini client + Flask routes + CLI helpers
- `jarvis.desktop`: Tkinter desktop UI, controllers, motion/voice/camera
- `jarvis.config`: Centralized settings via environment variables
- `jarvis.utils`: Cross-cutting helper utilities

## 🔧 Configuration

Settings live in `jarvis.config.settings` and read environment variables:
- `GEMINI_API_KEY`, `GEMINI_MODEL`
- `FLASK_HOST`, `FLASK_PORT`, `FLASK_DEBUG`
- Desktop tuning values (gesture cooldown, timeouts, etc.)

## 🔄 Notes

- Static assets and templates now live under `src/jarvis/web/`.
- Entry scripts (`app.py`, `run_web.py`, `run_desktop.py`) ensure `./src` is on `PYTHONPATH` before importing `jarvis`.

