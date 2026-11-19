"""Ponto de entrada da API Flask. Não serve páginas HTML."""
import os

from flask import Flask, jsonify
from flask_cors import CORS

from api.routes.health import health_bp
from backend.database import initialize_database


def create_app():
    app = Flask(__name__)

    # Origens permitidas durante o desenvolvimento com Live Server.
    allowed_origins = os.getenv(
        "FRONTEND_ORIGINS",
        "http://127.0.0.1:5500,http://localhost:5500"
    ).split(",")
    CORS(app, resources={r"/api/*": {"origins": [origin.strip() for origin in allowed_origins]}})

    initialize_database()
    app.register_blueprint(health_bp, url_prefix="/api")

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Endpoint não encontrado."}), 404

    @app.errorhandler(500)
    def internal_error(_error):
        return jsonify({"error": "Erro interno do servidor."}), 500

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=True)
