"""Helpers compartilhados pelas rotas da API."""
from flask import request

from backend.errors import ApiError


def json_object():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        raise ApiError(400, "Envie um objeto JSON válido no corpo da requisição.")
    return payload
