"""Endpoints de cadastro e autenticação."""
from functools import wraps

from flask import Blueprint, g, jsonify, request

from api.routes.helpers import json_object
from backend.errors import ApiError
from backend.services import auth_service

auth_bp = Blueprint("auth", __name__)


def require_auth(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        authorization = request.headers.get("Authorization", "")
        scheme, separator, token = authorization.partition(" ")
        if not separator or scheme.lower() != "bearer" or not token.strip():
            raise ApiError(401, "Envie um token Bearer válido no cabeçalho Authorization.")
        row = auth_service.authenticate_token(token.strip())
        if row is None:
            raise ApiError(401, "Token inválido ou expirado.")
        g.current_user = auth_service.public_user(row)
        g.current_token_hash = row["token_hash"]
        return view(*args, **kwargs)
    return wrapped


@auth_bp.post("/register")
def register():
    result = auth_service.register(json_object())
    return jsonify(result), 201


@auth_bp.post("/login")
def login():
    result = auth_service.login(json_object())
    return jsonify(result), 200


@auth_bp.post("/logout")
@require_auth
def logout():
    auth_service.revoke_token(g.current_token_hash)
    return jsonify({"message": "Sessão encerrada."}), 200


@auth_bp.get("/me")
@require_auth
def me():
    return jsonify({"user": g.current_user}), 200
