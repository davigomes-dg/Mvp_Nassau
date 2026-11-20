"""Validação e persistência do perfil ENEM de cada estudante."""
import math
import re

from backend.database import get_connection
from backend.errors import ApiError

SCORE_FIELDS = {
    "linguagens": "linguagens",
    "ciencias_humanas": "ciencias_humanas",
    "ciencias_natureza": "ciencias_natureza",
    "matematica": "matematica",
    "redacao": "redacao",
}
LOCATION_FIELDS = {"cidade": "cidade", "estado": "estado"}
STATE_PATTERN = re.compile(r"^[A-Z]{2}$")
BRAZIL_STATES = {
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS",
    "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC",
    "SP", "SE", "TO",
}


def _clean_score(value, field):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ApiError(400, "Revise os campos enviados.", {field: "Informe uma nota numérica entre 0 e 1000."})
    if value < 0 or value > 1000 or (isinstance(value, float) and not math.isfinite(value)):
        raise ApiError(400, "Revise os campos enviados.", {field: "A nota deve estar entre 0 e 1000."})
    return value


def _clean_location_value(value, field):
    if value is None:
        return None
    if not isinstance(value, str):
        raise ApiError(400, "Revise os campos enviados.", {field: "Informe um texto ou null para limpar o campo."})

    cleaned = value.strip()
    if field == "cidade":
        if not cleaned or len(cleaned) > 120:
            raise ApiError(400, "Revise os campos enviados.", {field: "A cidade deve ter entre 1 e 120 caracteres."})
        return cleaned

    cleaned = cleaned.upper()
    if not STATE_PATTERN.fullmatch(cleaned) or cleaned not in BRAZIL_STATES:
        raise ApiError(400, "Revise os campos enviados.", {field: "Informe uma sigla de estado válida, como CE."})
    return cleaned


def _profile_fields(payload):
    allowed_sections = {"notas", "localizacao"}
    extra_sections = set(payload) - allowed_sections
    if extra_sections:
        raise ApiError(400, "Revise os campos enviados.", {"fields": "Use somente notas e localizacao."})

    fields = {}
    for section, allowed_fields, cleaner in (
        ("notas", SCORE_FIELDS, _clean_score),
        ("localizacao", LOCATION_FIELDS, _clean_location_value),
    ):
        if section not in payload:
            continue
        values = payload[section]
        if not isinstance(values, dict):
            raise ApiError(400, "Revise os campos enviados.", {section: "Informe um objeto JSON."})

        extra_fields = set(values) - set(allowed_fields)
        if extra_fields:
            raise ApiError(400, "Revise os campos enviados.", {section: "Há campos não reconhecidos."})

        for field, value in values.items():
            fields[allowed_fields[field]] = cleaner(value, field)

    if not fields:
        raise ApiError(400, "Informe ao menos uma nota ou dado de localização para salvar.")
    return fields


def _serialize_profile(row):
    return {
        "notas": {field: row[field] for field in SCORE_FIELDS},
        "localizacao": {field: row[field] for field in LOCATION_FIELDS},
        "updated_at": row["updated_at"],
    }


def get_profile(user_id):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT linguagens, ciencias_humanas, ciencias_natureza, matematica, redacao, "
            "cidade, estado, updated_at FROM student_profiles WHERE user_id = ?",
            (user_id,),
        ).fetchone()

    if row is None:
        return {
            "profile": {
                "notas": {field: None for field in SCORE_FIELDS},
                "localizacao": {field: None for field in LOCATION_FIELDS},
                "updated_at": None,
            }
        }
    return {"profile": _serialize_profile(row)}


def update_profile(user_id, payload):
    fields = _profile_fields(payload)
    columns = list(fields)
    assignments = ", ".join(f"{column} = ?" for column in columns)
    values = [fields[column] for column in columns]

    with get_connection() as connection:
        connection.execute(
            "INSERT INTO student_profiles (user_id) VALUES (?) "
            "ON CONFLICT(user_id) DO NOTHING",
            (user_id,),
        )
        connection.execute(
            f"UPDATE student_profiles SET {assignments}, updated_at = CURRENT_TIMESTAMP "
            "WHERE user_id = ?",
            (*values, user_id),
        )
        row = connection.execute(
            "SELECT linguagens, ciencias_humanas, ciencias_natureza, matematica, redacao, "
            "cidade, estado, updated_at FROM student_profiles WHERE user_id = ?",
            (user_id,),
        ).fetchone()

    return {"profile": _serialize_profile(row)}
