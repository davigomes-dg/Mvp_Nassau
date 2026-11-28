"""Cadastro, login e validação de tokens de acesso."""
from hashlib import sha256
import re
import secrets
import time

from werkzeug.security import check_password_hash, generate_password_hash

from backend.database import get_connection
from backend.errors import ApiError

TOKEN_TTL_SECONDS = 7 * 24 * 60 * 60
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def _clean_text(value, field, maximum):
    if not isinstance(value, str):
        raise ApiError(400, "Revise os campos enviados.", {field: "Informe um texto."})
    cleaned = value.strip()
    if not cleaned or len(cleaned) > maximum:
        raise ApiError(
            400,
            "Revise os campos enviados.",
            {field: f"O campo é obrigatório e deve ter até {maximum} caracteres."},
        )
    return cleaned


def normalize_email(value):
    email = _clean_text(value, "email", 254).lower()
    if not EMAIL_PATTERN.fullmatch(email):
        raise ApiError(400, "Revise os campos enviados.", {"email": "Informe um e-mail válido."})
    return email


def _password(value):
    if not isinstance(value, str) or not 8 <= len(value) <= 128:
        raise ApiError(
            400,
            "Revise os campos enviados.",
            {"password": "A senha deve ter entre 8 e 128 caracteres."},
        )
    return value


def _new_access_token():
    token = secrets.token_urlsafe(32)
    return token, sha256(token.encode("utf-8")).hexdigest()


def public_user(row):
    return {"id": row["id"], "name": row["full_name"], "email": row["email"]}


def register(payload):
    name = _clean_text(payload.get("name"), "name", 120)
    email = normalize_email(payload.get("email"))
    password = _password(payload.get("password"))
    token, token_hash = _new_access_token()
    now = int(time.time())
    try:
        with get_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO users (full_name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, generate_password_hash(password)),
            )
            user_id = cursor.lastrowid
            connection.execute(
                "INSERT INTO auth_tokens (token_hash, user_id, expires_at) VALUES (?, ?, ?)",
                (token_hash, user_id, now + TOKEN_TTL_SECONDS),
            )
            user = connection.execute(
                "SELECT id, full_name, email FROM users WHERE id = ?", (user_id,)
            ).fetchone()
    except Exception as error:
        
        if "UNIQUE constraint failed: users.email" in str(error):
            raise ApiError(409, "Este e-mail já está cadastrado.") from error
        raise
    return {"user": public_user(user), "access_token": token, "token_type": "Bearer", "expires_in": TOKEN_TTL_SECONDS}


def login(payload):
    email = normalize_email(payload.get("email"))
    password = payload.get("password")
    if not isinstance(password, str) or not password:
        raise ApiError(400, "Revise os campos enviados.", {"password": "Informe a senha."})

    with get_connection() as connection:
        user = connection.execute(
            "SELECT id, full_name, email, password_hash FROM users WHERE email = ?", (email,)
        ).fetchone()
        if user is None or not check_password_hash(user["password_hash"], password):
            raise ApiError(401, "E-mail ou senha inválidos.")

        token, token_hash = _new_access_token()
        now = int(time.time())
        connection.execute("DELETE FROM auth_tokens WHERE expires_at <= ?", (now,))
        connection.execute(
            "INSERT INTO auth_tokens (token_hash, user_id, expires_at) VALUES (?, ?, ?)",
            (token_hash, user["id"], now + TOKEN_TTL_SECONDS),
        )
    return {"user": public_user(user), "access_token": token, "token_type": "Bearer", "expires_in": TOKEN_TTL_SECONDS}


def authenticate_token(token):
    token_hash = sha256(token.encode("utf-8")).hexdigest()
    with get_connection() as connection:
        row = connection.execute(
            "SELECT u.id, u.full_name, u.email, t.token_hash "
            "FROM auth_tokens t JOIN users u ON u.id = t.user_id "
            "WHERE t.token_hash = ? AND t.expires_at > ?",
            (token_hash, int(time.time())),
        ).fetchone()
    return row


def revoke_token(token_hash):
    with get_connection() as connection:
        connection.execute("DELETE FROM auth_tokens WHERE token_hash = ?", (token_hash,))
