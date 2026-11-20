# Projeto MVP — cadastro, autenticação e perfil do estudante

Esta versão permite criar uma conta, autenticar o estudante e salvar ou atualizar
as notas do ENEM e a localização associadas à conta. A comparação com cursos,
instituições e notas de corte ainda depende do cadastro desses dados e não faz
parte desta etapa.

## O que esta parte faz

- Cria usuários com nome, e-mail e senha.
- Valida os campos obrigatórios e impede e-mails duplicados.
- Armazena a senha como hash seguro do Werkzeug, nunca em texto puro.
- Faz login e fornece um token Bearer com validade de 7 dias.
- Protege as rotas privadas e permite revogar o token no logout.
- Retorna os dados básicos da conta autenticada sem expor o hash da senha.
- Salva e atualiza, por usuário, as cinco notas do ENEM, cidade e estado.
- Permite consultar o perfil autenticado e atualizar apenas os campos enviados.

## Arquivos principais

- `api/routes/auth.py`: endpoints e proteção Bearer.
- `api/routes/profile.py`: consulta e atualização do perfil protegido.
- `backend/services/auth_service.py`: validação, hash de senha e ciclo do token.
- `backend/services/profile_service.py`: validação e persistência das notas e localização.
- `backend/database.py`: conexão SQLite e inicialização do banco.
- `data/schema.sql`: tabelas de usuários, tokens e perfis dos estudantes.
- `frontend/`: telas de cadastro/login e edição do perfil.

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

### Usar no VS Code

Abra a pasta `Projeto-Mvp` no VS Code e instale a extensão **Python** da
Microsoft (`ms-python.python`). Selecione o interpretador da pasta `.venv` pelo
comando **Python: Select Interpreter**. A configuração de execução do projeto
também fica disponível ao pressionar `F5`; para o front-end, abra
`frontend/index.html` com o Live Server.

## Endpoints

| Método | Rota | Acesso | O que faz |
|---|---|---|---|
| GET | `/api/health` | Público | Confirma que a API está disponível |
| POST | `/api/auth/register` | Público | Cria usuário e inicia sessão (201) |
| POST | `/api/auth/login` | Público | Autentica e inicia sessão |
| POST | `/api/auth/logout` | Bearer | Revoga o token atual |
| GET | `/api/auth/me` | Bearer | Consulta o usuário autenticado |
| GET | `/api/profile` | Bearer | Consulta as notas e a localização do estudante |
| PUT | `/api/profile` | Bearer | Cria ou atualiza os campos enviados do perfil |

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

## Perfil do estudante

Envie um token Bearer para consultar ou atualizar o perfil. As notas são
opcionais e aceitam valores numéricos de 0 a 1000. A localização é armazenada
como cidade e sigla do estado (UF). Campos omitidos em uma atualização parcial
mantêm seus valores; envie `null` para limpar um campo.

```http
PUT /api/profile
Authorization: Bearer <access_token>
Content-Type: application/json
```

```json
{
  "notas": {
    "linguagens": 628.4,
    "ciencias_humanas": 650,
    "ciencias_natureza": 702.1,
    "matematica": 741.8,
    "redacao": 880
  },
  "localizacao": {
    "cidade": "Fortaleza",
    "estado": "CE"
  }
}
```

`GET /api/profile` retorna os mesmos campos dentro de `profile`. Se o estudante
ainda não salvou dados, os campos são retornados como `null`. Cada perfil é
vinculado ao usuário autenticado e é removido automaticamente se a conta for
excluída.

O token original é retornado uma única vez e não é guardado no banco. O SQLite
armazena apenas seu hash SHA-256. O logout remove esse token, que deixa de ser
aceito nas próximas chamadas.

## Banco de dados

`data/schema.sql` define `users`, `auth_tokens` e `student_profiles`, incluindo
unicidade de e-mail, chaves estrangeiras e expiração dos tokens. A tabela do
perfil é criada também em um banco existente na próxima inicialização da API. O
arquivo `data/database.db` é gerado localmente e fica fora do controle de versão.

## Respostas de erro

Erros são retornados em JSON. Exemplos de códigos: 400 para campos inválidos,
401 para credenciais ou token inválidos, 409 para e-mail já cadastrado e 404 para
rota inexistente.
