# Projeto MVP — Parte 1: cadastro e autenticação

Esta versão contém somente a primeira parte do back-end: cadastro de usuário,
login, logout e consulta da conta autenticada. O perfil ENEM e os resultados não
fazem parte deste pacote.

## O que esta parte faz

- Cria usuários com nome, e-mail e senha.
- Valida os campos obrigatórios e impede e-mails duplicados.
- Armazena a senha como hash seguro do Werkzeug, nunca em texto puro.
- Faz login e fornece um token Bearer com validade de 7 dias.
- Protege as rotas privadas e permite revogar o token no logout.
- Retorna os dados básicos da conta autenticada sem expor o hash da senha.

## Arquivos principais

- `api/routes/auth.py`: endpoints e proteção Bearer.
- `backend/services/auth_service.py`: validação, hash de senha e ciclo do token.
- `backend/database.py`: conexão SQLite e inicialização do banco.
- `data/schema.sql`: tabelas de usuários e tokens.

## Executar

Requer Python 3.10 ou superior. Na raiz `Projeto-Mvp`, execute:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m backend.app
```

No Linux/macOS, use `python3 -m venv .venv`, ative com
`source .venv/bin/activate` e execute `python -m backend.app`. A API inicia em
`http://127.0.0.1:5000`. As tabelas são criadas na primeira execução. O Front-end
continua separado e pode ser servido pelo Live Server.

## Endpoints

| Método | Rota | Acesso | O que faz |
|---|---|---|---|
| GET | `/api/health` | Público | Confirma que a API está disponível |
| POST | `/api/auth/register` | Público | Cria usuário e inicia sessão (201) |
| POST | `/api/auth/login` | Público | Autentica e inicia sessão |
| POST | `/api/auth/logout` | Bearer | Revoga o token atual |
| GET | `/api/auth/me` | Bearer | Consulta o usuário autenticado |

## Cadastro

Envie um objeto JSON:

```http
POST /api/auth/register
Content-Type: application/json
```

```json
{"name":"Ana Silva","email":"ana@example.com","password":"senha-com-8-ou-mais"}
```

A resposta contém `user`, `access_token`, `token_type` e `expires_in`. O cadastro
já inicia a sessão. A senha deve ter de 8 a 128 caracteres. Os e-mails são
normalizados para minúsculas.

## Login e uso do token

Envie `email` e `password` para `POST /api/auth/login`. Para chamar `/api/auth/me`
ou `/api/auth/logout`, envie o token recebido no cadastro ou login:

```http
Authorization: Bearer <access_token>
```

Exemplo com `fetch()`:

```javascript
const response = await fetch("http://127.0.0.1:5000/api/auth/me", {
  headers: { Authorization: `Bearer ${token}` },
});
const data = await response.json();
```

O token original é retornado uma única vez e não é guardado no banco. O SQLite
armazena apenas seu hash SHA-256. O logout remove esse token, que deixa de ser
aceito nas próximas chamadas.

## Banco de dados

`data/schema.sql` define somente `users` e `auth_tokens`, incluindo unicidade de
e-mail, chave estrangeira e expiração dos tokens. O arquivo `data/database.db`
veio vazio no projeto original; as tabelas serão criadas quando a API iniciar.

## Respostas de erro

Erros são retornados em JSON. Exemplos de códigos: 400 para campos inválidos,
401 para credenciais ou token inválidos, 409 para e-mail já cadastrado e 404 para
rota inexistente.
