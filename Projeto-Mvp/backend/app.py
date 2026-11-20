"""Ponto de entrada da API Flask. O Flask não serve páginas HTML."""
import os

from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from api.routes.auth import auth_bp
from api.routes.health import health_bp
from api.routes.profile import profile_bp
from backend.database import initialize_database
from backend.errors import ApiError


def create_app():
    app = Flask(__name__)
    allowed_origins = [
        origin.strip()
        for origin in os.getenv(
            "FRONTEND_ORIGINS",
            "http://127.0.0.1:5500,http://localhost:5500",
        ).split(",")
        if origin.strip()
    ]
    CORS(
        app,
        resources={r"/api/*": {"origins": allowed_origins}},
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "OPTIONS"],
    )

    initialize_database()
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(profile_bp, url_prefix="/api")

    @app.errorhandler(ApiError)
    def api_error(error):
        body = {"error": error.message}
        if error.details is not None:
            body["details"] = error.details
        return jsonify(body), error.status_code

    @app.errorhandler(HTTPException)
    def http_error(error):
        return jsonify({"error": error.name}), error.code

    @app.errorhandler(500)
    def internal_error(_error):
        app.logger.exception("Erro interno ao processar requisição")
        return jsonify({"error": "Erro interno do servidor."}), 500

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(
        host=os.getenv("HOST", "127.0.0.1"),
        port=port,
        debug=os.getenv("FLASK_DEBUG", "0") == "1",
    )
