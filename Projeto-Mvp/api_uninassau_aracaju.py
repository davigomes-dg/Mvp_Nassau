from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="API UNINASSAU Aracaju",
    description="API de cursos e simulação com notas do ENEM para unidade de Aracaju/SE.",
    version="1.0.0",
)

# Permite que o frontend (ex.: Live Server em http://127.0.0.1:5500 ou :3000) acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, troque pelo domínio exato do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
FACULDADE_ARACAJU = {
    "instituicao": "UNINASSAU",
    "unidade": "Aracaju",
    "cidade": "Aracaju",
    "uf": "SE",
    "cursos": [
        {
            "id": "ads",
            "nome": "Análise e Desenvolvimento de Sistemas",
            "turno": "Noite",
            "nota_corte_referencia": 580.0,
            "pesos": {
                "linguagens": 1,
                "humanas": 1,
                "natureza": 1,
                "matematica": 3,
                "redacao": 2,
            },
        },
        {
            "id": "direito",
            "nome": "Direito",
            "turno": "Manhã / Noite",
            "nota_corte_referencia": 650.0,
            "pesos": {
                "linguagens": 2,
                "humanas": 2,
                "natureza": 1,
                "matematica": 1,
                "redacao": 3,
            },
        },
        {
            "id": "psicologia",
            "nome": "Psicologia",
            "turno": "Noite",
            "nota_corte_referencia": 640.0,
            "pesos": {
                "linguagens": 2,
                "humanas": 2,
                "natureza": 1,
                "matematica": 1,
                "redacao": 2,
            },
        },
    ],
}


class NotasEnemInput(BaseModel):
    linguagens: float = Field(..., ge=0, le=1000)
    humanas: float = Field(..., ge=0, le=1000)
    natureza: float = Field(..., ge=0, le=1000)
    matematica: float = Field(..., ge=0, le=1000)
    redacao: float = Field(..., ge=0, le=1000)
    cidade: str | None = "Aracaju"
    uf: str | None = "SE"


@app.get("/")
def info_faculdade():
    return {
        "instituicao": FACULDADE_ARACAJU["instituicao"],
        "unidade": FACULDADE_ARACAJU["unidade"],
        "cidade": FACULDADE_ARACAJU["cidade"],
        "uf": FACULDADE_ARACAJU["uf"],
        "total_cursos": len(FACULDADE_ARACAJU["cursos"]),
    }


@app.get("/cursos")
def listar_cursos(turno: str | None = None):
    cursos = FACULDADE_ARACAJU["cursos"]
    if turno:
        cursos = [c for c in cursos if turno.lower() in c["turno"].lower()]
    return {"unidade": "Aracaju / SE", "cursos": cursos}


@app.get("/cursos/{curso_id}")
def detalhar_curso(curso_id: str):
    for curso in FACULDADE_ARACAJU["cursos"]:
        if curso["id"] == curso_id.lower():
            return curso
    raise HTTPException(status_code=404, detail="Curso não encontrado.")


@app.post("/simular")
def simular_cursos(payload: NotasEnemInput):
    notas = {
        "linguagens": payload.linguagens,
        "humanas": payload.humanas,
        "natureza": payload.natureza,
        "matematica": payload.matematica,
        "redacao": payload.redacao,
    }

    simulacoes = []
    for curso in FACULDADE_ARACAJU["cursos"]:
        pesos = curso["pesos"]
        media_ponderada = round(
            sum(notas[area] * pesos[area] for area in pesos) / sum(pesos.values()),
            2,
        )
        corte = curso["nota_corte_referencia"]
        diferenca = round(media_ponderada - corte, 2)

        simulacoes.append({
            "curso_id": curso["id"],
            "curso": curso["nome"],
            "turno": curso["turno"],
            "media_ponderada": media_ponderada,
            "nota_corte_referencia": corte,
            "alcanca_corte": media_ponderada >= corte,
            "diferenca_pontos": diferenca,
        })

    return {
        "unidade": "Aracaju / SE",
        "local_informado": f"{payload.cidade or ''} - {payload.uf or ''}".strip(" -"),
        "resultados": simulacoes,
    }