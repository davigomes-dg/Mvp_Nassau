-- MVP: contas, tokens de autenticação e perfis dos estudantes.
-- Nenhuma senha em texto puro ou token original é armazenado.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL CHECK (length(trim(full_name)) BETWEEN 1 AND 120),
    email TEXT NOT NULL COLLATE NOCASE UNIQUE CHECK (length(email) <= 254),
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS auth_tokens (
    token_hash TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_auth_tokens_user ON auth_tokens(user_id);
CREATE INDEX IF NOT EXISTS idx_auth_tokens_expiry ON auth_tokens(expires_at);

CREATE TABLE IF NOT EXISTS student_profiles (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    linguagens REAL CHECK (linguagens IS NULL OR linguagens BETWEEN 0 AND 1000),
    ciencias_humanas REAL CHECK (ciencias_humanas IS NULL OR ciencias_humanas BETWEEN 0 AND 1000),
    ciencias_natureza REAL CHECK (ciencias_natureza IS NULL OR ciencias_natureza BETWEEN 0 AND 1000),
    matematica REAL CHECK (matematica IS NULL OR matematica BETWEEN 0 AND 1000),
    redacao REAL CHECK (redacao IS NULL OR redacao BETWEEN 0 AND 1000),
    cidade TEXT CHECK (cidade IS NULL OR length(trim(cidade)) BETWEEN 1 AND 120),
    estado TEXT CHECK (estado IS NULL OR length(estado) = 2),
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
