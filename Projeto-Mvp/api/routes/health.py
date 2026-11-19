"""Rota técnica para verificar se a API está disponível."""
from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "message": "API do Projeto MVP disponível."
    }), 200
