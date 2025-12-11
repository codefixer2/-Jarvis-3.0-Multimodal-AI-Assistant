"""Flask Web Application Entry Point"""
from pathlib import Path

from flask import Flask, render_template
from flask_cors import CORS

from jarvis.api.routes import register_routes
from jarvis.config.settings import FLASK_HOST, FLASK_PORT, FLASK_DEBUG

_BASE_DIR = Path(__file__).resolve().parent
_TEMPLATES_DIR = _BASE_DIR / "templates"
_STATIC_DIR = _BASE_DIR / "static"


def create_app() -> Flask:
    """Application factory for the Jarvis web app."""
    app = Flask(
        __name__,
        template_folder=str(_TEMPLATES_DIR),
        static_folder=str(_STATIC_DIR),
    )
    CORS(app)

    # Register API routes
    register_routes(app)

    @app.route("/")
    def index():
        """Render the main index page"""
        return render_template("index.html")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT)
