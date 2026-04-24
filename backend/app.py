from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_session import Session
from flask_cors import CORS
import os

from routes.docs_routes import docs_bp
from routes.ai_routes import ai_bp


def _get_bool_env(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_cors_origins():
    raw_value = (
        os.getenv("CORS_ORIGINS")
        or os.getenv("FRONTEND_URL")
        or "http://localhost:5173"
    )

    return [
        origin.strip().rstrip("/")
        for origin in raw_value.split(",")
        if origin.strip()
    ]


def create_app():
    app = Flask(__name__)

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")

    # 🔐 Config
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "smartdocs-secret-key")
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_USE_SIGNER"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    app.config["SESSION_COOKIE_SECURE"] = _get_bool_env("SESSION_COOKIE_SECURE", False)
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["FRONTEND_URL"] = frontend_url

    # 🔥 IMPORTANT FOR RENDER (avoid session folder issues)
    os.makedirs("flask_session", exist_ok=True)

    Session(app)

    # 🌐 CORS
    CORS(
        app,
        supports_credentials=True,
        origins=_get_cors_origins()
    )

    # 📦 Routes
    app.register_blueprint(docs_bp)
    app.register_blueprint(ai_bp)

    # ❤️ Health check (VERY IMPORTANT FOR RENDER)
    @app.get("/")
    def home():
        return "Smart Docs Backend Running 🚀", 200

    @app.get("/health")
    def health():
        return {"ok": True}, 200

    return app


# 👇 REQUIRED FOR GUNICORN
app = create_app()


# 👇 LOCAL RUN ONLY
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render prefers 10000 fallback
    app.run(host="0.0.0.0", port=port, debug=False)
