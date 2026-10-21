import pandas as pd
import numpy as np
import uuid
import metodos as m
from sklearn import metrics as me
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

from sklearn.preprocessing import StandardScaler

CACHE = {}

def teste():
    return {"mensagem": "Teste realizado com sucesso"}

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

def metricas(texto,y_teste,y_pred):
    mae = me.mean_absolute_error(y_teste, y_pred)
    mse = me.mean_squared_error(y_teste, y_pred)
    rmse = np.sqrt(mse)
    r2 = me.r2_score(y_teste, y_pred)
    print("\n------------------------------------",texto)
    print("------------------------------------")
    print(f"MAE ...............: {mae:.4f}")
    print(f"MSE ...............: {mse:.4f}")
    print(f"RMSE ..............: {rmse:.4f}")
    print(f"R² ................: {r2:.4f}")

    return [{
        "modelo": texto,
        "mae": round(float(mae), 4),
        "mse": round(float(mse), 4),
        "rmse": round(float(rmse), 4),
        "r2": round(float(r2), 4),
    }]    

# -----------------------------------------------
# MÉTODOS 
# -----------------------------------------------

def gradient_boosting_treino(x_train, y_train, parametros=None):
    p = [300, 0.1, 4, 0.8, 10]
    
    if parametros:
        p = list(parametros) + p[len(parametros):]
    
    gb_model = GradientBoostingRegressor(
        n_estimators=p[0],
        learning_rate=p[1],
        max_depth=p[2],
        subsample=p[3],
        min_samples_leaf=p[4],
    )

    gb_model.fit(x_train, y_train)
    return gb_model

def gradient_boosting_teste(x_teste, y_teste, gb_model):
    y_pred = gb_model.predict(x_teste)
    return metricas("GRADIENT BOOSTING", y_teste, y_pred)

# =============================================================
# MÉTODO PRINCIPAL
# =============================================================
def main(arq: str, metodo: str, parametros: str, test: float):
    parametros = ler_parametros(parametros) if parametros and parametros.filename else None

    feat, target, df, indice_alvo = ler_arquivo(arq)

    dataset_id = str(uuid.uuid4())
    CACHE[dataset_id] = df

    dados_dataset = (
        df.head(50)
        .round(4)
        .astype(object)
        .where(df.head(50).notna(), None)
        .values.tolist()
    )

    x_treino, x_teste, y_treino, y_teste = train_test_split(
        feat, target, test_size=test, random_state=42
    )

    scaler = StandardScaler()
    x_treino_sc = scaler.fit_transform(x_treino)
    x_teste_sc = scaler.transform(x_teste)
    
    resultados = []

    if metodo == "gradient_boosting":
        modelo = gradient_boosting_treino(x_treino_sc,y_treino, parametros)
        retorno = gradient_boosting_teste(x_teste_sc,y_teste,modelo)

        resultados.extend(retorno)

    elif metodo == "lasso":
        modelo = "funcao_treino"
        "funcao_test"

    elif metodo == "bagging":
        modelo = "funcao_treino"
        "funcao_test"

    elif metodo == "svr":
        modelo = "funcao_treino"
        "funcao_test"

    elif metodo == "huber_regressor":
        modelo = "funcao_treino"
        "funcao_test"

    elif metodo == "knn":
        modelo = "funcao_treino"
        "funcao_test"

    elif metodo == "extra_trees":
        modelo = "funcao_treino"
        "funcao_test"

    elif metodo == "ridge":
        modelo = "funcao_treino"
        "funcao_test"

    elif metodo == "sgd_regressor":
        modelo = "funcao_treino"
        "funcao_test"

    elif metodo == "bayesian_ridge":
        modelo = "funcao_treino"
        "funcao_test"

    elif metodo == "decision_tree":
        modelo = "funcao_treino"
        "funcao_test"

    elif metodo == "regressao_linear":
        modelo = "funcao_treino"
        "funcao_test"

    elif modelo == "hist_gradient_boosting":
        modelo = "funcao_treino"
        "funcao_test"    
    
    elif modelo == "kernel_ridge":
        modelo = "funcao_treino"
        "funcao_test"

    elif metodo == "adaboost":
        modelo = "funcao_treino"
        "funcao_test"

    elif metodo == "elastic_net":
        modelo = "funcao_treino"
        "funcao_test"
     
    elif metodo == "random_forest":
        modelo = "funcao_treino"
        "funcao_test"

    else:
        raise ValueError("Método não informado.")

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
        "resultados": resultados,
    }

def buscar_linhas(dataset_id: str, offset: int, limit: int):
    df = CACHE.get(dataset_id)
    if df is None:
        return None
    parte = df.iloc[offset:offset + limit].round(4)
    linhas = parte.astype(object).where(parte.notna(), None).values.tolist()
    return {"linhas": linhas, "total": int(len(df))}