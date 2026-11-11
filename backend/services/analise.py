import os
import math
import json
import hashlib
import threading
import numpy as np
import pandas as pd
from services import metodos as me
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

CACHE = {}
TRAVA = threading.Lock()
ARQUIVO_HISTORICO = os.environ.get("HISTORICO_PATH", "data/historico.json")

def _limpar(v):
    if hasattr(v, "item"):
        v = v.item()
    if isinstance(v, float) and not math.isfinite(v):
        return None
    return v

def _historico_limpo():
    return [{k: _limpar(v) for k, v in r.items()} for r in HISTORICO]

def _carregar():
    try:
        with open(ARQUIVO_HISTORICO, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _json_seguro(o):
    return o.item() if hasattr(o, "item") else str(o)


def _salvar():
    pasta = os.path.dirname(ARQUIVO_HISTORICO)
    if pasta:
        os.makedirs(pasta, exist_ok=True)
    tmp = ARQUIVO_HISTORICO + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(HISTORICO, f, ensure_ascii=False, default=_json_seguro)
    os.replace(tmp, ARQUIVO_HISTORICO)


HISTORICO = _carregar()

def ler_arquivo(arquivo):
    indice_alvo = int(float(pd.read_csv(arquivo.file, header=None, nrows=1).iloc[0, 0])) - 1
    arquivo.file.seek(0)

    df = pd.read_csv(arquivo.file, header=1)

    atributos_df = df.drop(columns=df.columns[indice_alvo])
    atributos = pd.get_dummies(atributos_df, dtype=int).astype(float).values

    target = df.iloc[:, indice_alvo]

    if pd.api.types.is_numeric_dtype(target):
        target = target.values
    else:
        target = target.astype("category").cat.codes.values

    return atributos, target, df, indice_alvo

def converter(v):
    v = v.strip()
    baixo = v.lower()

    if baixo == "true":
        return True
    if baixo == "false":
        return False

    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass

    return v

def ler_parametros(parametros):
    texto = parametros.file.read().decode("utf-8-sig").strip()
    valores = texto.replace("\n", ",").replace("\r", "").split(",")

    print("texto", texto)
    return [converter(v) for v in valores if v.strip() != ""]

def como_lista(r):
    if isinstance(r, tuple):
        r = r[0]
    print(f"como_lista: {type(r)}")
    return [r] if isinstance(r, dict) else list(r)


def registrar(linhas, nome_arquivo):
    with TRAVA:
        for nova in linhas:
            nova["arquivo"] = nome_arquivo
            HISTORICO.append(nova)
        _salvar()
        return _historico_limpo()

# =============================================================
# MÉTODO PRINCIPAL
# =============================================================
def main(arq, metodo, parametros, test):
    parametros = ler_parametros(parametros) if parametros and parametros.filename else None

    conteudo = arq.file.read()
    arq.file.seek(0)

    dataset_id = hashlib.md5(conteudo).hexdigest()

    feat, target, df, indice_alvo = ler_arquivo(arq)
    CACHE[dataset_id] = df

    dados_dataset = (
        df.head(50).round(4).astype(object)
        .where(df.head(50).notna(), None).values.tolist()
    )

    x_treino, x_teste, y_treino, y_teste = train_test_split(
        feat, target, test_size=test, random_state=42
    )
    scaler = StandardScaler()
    x_treino_sc = scaler.fit_transform(x_treino)
    x_teste_sc = scaler.transform(x_teste)

    treino = getattr(me, f"{metodo}_treino", None)
    teste_func = getattr(me, f"{metodo}_teste", None)

    if not callable(treino) or not callable(teste_func):
        raise ValueError(
            f"Funções do método '{metodo}' não encontradas."
        )

    modelo = treino(x_treino_sc, y_treino, parametros)

    retorno = teste_func(x_teste_sc, y_teste, modelo)

    novas = []

    for linha in como_lista(retorno):
        linha = {k: _limpar(v) for k, v in dict(linha).items()}
        linha["metodo"] = metodo
        linha["versao"] = (
            "Personalizada" if parametros is not None else "Padrão"
        )
        linha["parametros"] = (
            str(parametros) if parametros is not None else "padrão"
        )
        novas.append(linha)

    historico = registrar(novas, arq.filename)

    return {
        "dataset_id": dataset_id,
        "indice_alvo": indice_alvo,
        "dataset": arq.filename,
        "registros": int(len(feat)),
        "colunas": int(feat.shape[1] + 1),
        "teste": test,
        "método": metodo,
        "colunas_nomes": [str(c) for c in df.columns],
        "dadosDataset": dados_dataset,
        "resultados": historico,
    }

def buscar_linhas(dataset_id: str, offset: int, limit: int):
    df = CACHE.get(dataset_id)
    if df is None:
        return None
    parte = df.iloc[offset:offset + limit].round(4)
    linhas = parte.astype(object).where(parte.notna(), None).values.tolist()
    return {"linhas": linhas, "total": int(len(df))}

def buscar_historico():
    with TRAVA:
        return _historico_limpo()

def limpar_historico():
    with TRAVA:
        HISTORICO.clear()
        _salvar()
