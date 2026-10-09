from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Template Dataset API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def raiz():
    return {"mensagem": "API funcionando"}


@app.get("/api/health")
def saude():
    return {"status": "ok"}

@app.post("/api/executar")
def executar():
    return {"mensagem": "Arquivo aberto com sucesso"}