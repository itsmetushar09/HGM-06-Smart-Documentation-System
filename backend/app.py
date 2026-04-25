from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from flask_session import Session
import os
from routes.auth_routes import auth_bp
from routes.docs_routes import docs_bp
from flask_cors import CORS
from routes.ai_routes import ai_bp

def create_app():

    app = Flask(__name__)
    
    # Get CORS origins from env
    cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    is_production = os.getenv("FLASK_ENV") == "production"

    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY","smartdocs-secret-key")
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_PREMANENT"]=False
    app.config["SESSION_USE_SIGNER"]=True
    app.config["SESSION_COOKIE_SAMESITE"]="Lax"
    app.config["SESSION_COOKIE_SECURE"]=is_production
    app.config["SESSION_COOKIE_HTTPONLY"]=True
    

    Session(app)
    CORS(app, supports_credentials=True, origins=cors_origins)

    app.register_blueprint(auth_bp)
    app.register_blueprint(docs_bp)
    app.register_blueprint(ai_bp)

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    app.run(host="0.0.0.0", debug=False, port=port)
