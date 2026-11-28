"""Endpoints privados do perfil do estudante."""
from flask import Blueprint, g, jsonify

from api.routes.auth import require_auth
from api.routes.helpers import json_object
from backend.services import profile_service

profile_bp = Blueprint("profile", __name__)


@profile_bp.get("/profile")
@require_auth
def get_profile():
    return jsonify(profile_service.get_profile(g.current_user["id"])), 200


@profile_bp.put("/profile")
@require_auth
def update_profile():
    result = profile_service.update_profile(g.current_user["id"], json_object())
    return jsonify(result), 200
