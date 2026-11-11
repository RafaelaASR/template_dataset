from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.analise import main, buscar_linhas, buscar_historico, limpar_historico


app = FastAPI()

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
async def executar(
        arquivo: UploadFile = File(...),
        metodo: str = Form(...),
        teste: float = Form(0.2),
        parametros: UploadFile | None = File(None),
    ):    
    resultado = main(arquivo, metodo, parametros, teste)
    return resultado

@app.get("/api/dataset/{dataset_id}")
def carregar_mais(dataset_id: str, offset: int = 0, limit: int = 50):
    resposta = buscar_linhas(dataset_id, offset, limit)
    if resposta is None:
        raise HTTPException(status_code=404, detail="Dataset expirado. Envie o arquivo novamente.")
    return resposta

@app.get("/api/historico")
def historico():
    return {"resultados": buscar_historico()}

@app.delete("/api/historico")
def apagar_historico():
    limpar_historico()
    return {"resultados": []}