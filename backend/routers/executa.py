from fastapi import APIRouter
from services.analise import abrir_arquivo

router = APIRouter(prefix="/api")

@router.post("/executar")
def rota_executar():
    resultado = executar()
    return {"mensagem": "Arquivo aberto com sucesso", "dados": resultado}