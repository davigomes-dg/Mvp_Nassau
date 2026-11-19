"""Configuração e conexão com o banco de dados SQLite."""
from pathlib import Path
import sqlite3

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "database.db"
SCHEMA_PATH = PROJECT_ROOT / "data" / "schema.sql"


def get_connection():
    """Abre uma conexão SQLite com suporte a acesso por nome de coluna."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Executa o schema SQL, caso existam instruções de criação."""
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with get_connection() as connection:
        connection.executescript(schema)
