# -----------------------------------------------
# IMPORTS - adicione os imports que precisar
# -----------------------------------------------

from services import analise
from sklearn.ensemble import GradientBoostingRegressor
from services.metricas import metricas



# -----------------------------------------------
# MÉTODOS - adicione o método de treino e teste abaixo
# -----------------------------------------------

def gradient_boosting_treino(x_train, y_train, parametros=None):
    p = [300, 0.1, 4, 0.8, 10, 0]
    
    if parametros:
        p = list(parametros) + p[len(parametros):]
    
    gb_model = GradientBoostingRegressor(
        n_estimators=p[0],
        learning_rate=p[1],
        max_depth=p[2],
        subsample=p[3],
        min_samples_leaf=p[4],
        random_state=p[5]
    )

    gb_model.fit(x_train, y_train)
    return gb_model

def gradient_boosting_teste(x_teste, y_teste, gb_model):
    y_pred = gb_model.predict(x_teste)
    return metricas("GRADIENT BOOSTING", y_teste, y_pred)

