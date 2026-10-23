import hashlib
import threading
import pandas as pd
from services import metodos as me
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

CACHE = {}
HISTORICO = {}
TRAVA = threading.Lock()

def ler_arquivo(arquivo):
    indice_alvo = int(float(pd.read_csv(arquivo.file, header=None, nrows=1).iloc[0, 0])) - 1
    arquivo.file.seek(0)

    df = pd.read_csv(arquivo.file, header=1)
    atributos = df.drop(columns=df.columns[indice_alvo]).astype(float).values
    target = df.iloc[:, indice_alvo].astype(float).values

    return atributos, target, df, indice_alvo

def converter(v):
    v = v.strip()
    try:
        return int(v)
    except ValueError:
        return float(v)

def ler_parametros(parametros):
    texto = parametros.file.read().decode("utf-8-sig").strip()
    valores = texto.replace("\n", ",").replace("\r", "").split(",")
    return [converter(v) for v in valores if v.strip() != ""]

def como_lista(r):
    if isinstance(r, tuple):
        r = r[0]
    return [r] if isinstance(r, dict) else list(r)

def registrar(dataset_id, linhas):
    chave = lambda r: (
        r["modelo"],
        r.get("versao", "Padrão"),
        r.get("parametros", "padrão")
    )

    with TRAVA:
        hist = HISTORICO.setdefault(dataset_id, [])

        for nova in linhas:
            hist[:] = [
                r for r in hist
                if chave(r) != chave(nova)
            ]
            hist.append(nova)

        return list(hist)

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
        linha = dict(linha)
        linha["modelo"] = metodo
        linha["versao"] = (
            "Personalizada" if parametros is not None else "Padrão"
        )
        linha["parametros"] = (
            str(parametros) if parametros is not None else "padrão"
        )
        novas.append(linha)

    historico = registrar(dataset_id, novas)

    return {
        "dataset_id": dataset_id,
        "indice_alvo": indice_alvo,
        "dataset": arq.filename,
        "registros": int(len(feat)),
        "colunas": int(feat.shape[1] + 1),
        "teste": test,
        "metodo": metodo,
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