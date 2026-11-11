# -----------------------------------------------
# IMPORTS - adicione os imports que precisar
# -----------------------------------------------

from services import analise
from sklearn.ensemble import GradientBoostingRegressor
from services.metricas import metricas

from sklearn.kernel_ridge import KernelRidge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import BayesianRidge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.linear_model import Ridge

from sklearn.linear_model import Lasso
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.ensemble import BaggingRegressor
from sklearn.neighbors import KNeighborsRegressor

from sklearn.linear_model import HuberRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import SGDRegressor


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


# -----------------------------------------------
# Camila
# -----------------------------------------------

def kernel_ridge_treino(x_train, y_train, parametros=None):
    # Valores padrão: alpha, kernel, gamma
    p = [0.001, 'rbf', 0.3]  
    
    if parametros:
        p = list(parametros) + p[len(parametros):]
        
    # Instância do modelo Kernel Ridge
    kr_model = KernelRidge(
        alpha=p[0],  # Controla a regularização 
        kernel=p[1], # Tipo de kernel matemático
        gamma=p[2]   # Coeficiente para o kernel rbf
    )
    kr_model.fit(x_train, y_train)
    return kr_model

def kernel_ridge_teste(x_teste, y_teste, kr_model):
    y_pred = kr_model.predict(x_teste)
    return metricas("KERNEL RIDGE", y_teste, y_pred)


# -----------------------------------------------
# Pedro Nelson
# -----------------------------------------------


def linear_regression_treino(x_train, y_train, parametros=None):

    fit_intercept = True
    copy_X = True
    tol = 1e-6
    n_jobs = None
    positive = False
    
    lr_model = LinearRegression(
        fit_intercept=fit_intercept,
        copy_X=copy_X,
        tol=tol,
        n_jobs=n_jobs,
        positive=positive
    )

    lr_model.fit(x_train, y_train)
    return lr_model

def linear_regression_teste(x_teste, y_teste, lr_model):
    y_pred = lr_model.predict(x_teste)
    return metricas("REGRESSAO LINEAR", y_teste, y_pred)



# -----------------------------------------------
# Pedro Ernesto
# -----------------------------------------------


def decision_tree_treino(x_train, y_train, parametros=None):
    p = [5, 42]  # max_depth, random_state

    if parametros:
        p = list(parametros) + p[len(parametros):]

    dt_model = DecisionTreeRegressor(
        max_depth=p[0],
        random_state=p[1]
    )
    dt_model.fit(x_train, y_train)
    return dt_model


def decision_tree_teste(x_teste, y_teste, dt_model):
    y_pred = dt_model.predict(x_teste)
    return metricas("DECISION TREE", y_teste, y_pred)


# -----------------------------------------------
#  Felipe Monteiro
# -----------------------------------------------



def elastic_net_treino(x_train, y_train, parametros=None):

    p = [1.0, 0.5, 1000, 0.0001, 0]

    if parametros:
        p = list(parametros) + p[len(parametros):]

    elastic_model = ElasticNet(
        alpha=p[0],
        l1_ratio=p[1],
        max_iter=p[2],
        tol=p[3],
        random_state=p[4]
    )

    elastic_model.fit(x_train, y_train)

    return elastic_model

def elastic_net_teste(x_teste, y_teste, elastic_model):

    y_pred = elastic_model.predict(x_teste)

    return metricas("ELASTIC NET", y_teste, y_pred)



# -----------------------------------------------
#  Sávio
# -----------------------------------------------

def bayesian_ridge_treino(x_train, y_train, parametros=None):
     p = [300, 0.001, 1e-6, 1e-6, 1e-6, 1e-6, 1]

     if parametros:
         p = list(parametros) + p[len(parametros):]

     poly = PolynomialFeatures(degree=int(p[6]), include_bias=False)
     x_train_poly = poly.fit_transform(x_train)

     br_model = BayesianRidge(
         max_iter=int(p[0]),
         tol=p[1],
         alpha_1=p[2],
         alpha_2=p[3],
         lambda_1=p[4],
         lambda_2=p[5],
     )

     br_model.fit(x_train_poly, y_train)
     return poly, br_model

def bayesian_ridge_teste(x_teste, y_teste, modelo):
     poly, br_model = modelo
     y_pred = br_model.predict(poly.transform(x_teste))
     return metricas("BAYESIAN RIDGE", y_teste, y_pred)


# ----
# caio 
# ----

def ridge_treino(x_train, y_train, parametros=None):
    p = [1, True, True, None, 0.0001, 'auto', False]

    if parametros:
        p = list(parametros) + p[len(parametros):]


    rid_model = Ridge(
        random_state=42,
        alpha = p[0],
        fit_intercept = p[1],
        copy_X = p[2],
        max_iter = p[3],
        tol = p[4],
        solver = p[5],
        positive = p[6]
    )
    rid_model.fit(x_train, y_train)
    return rid_model

def ridge_teste(x_teste, y_teste, rid_model):
    y_pred = rid_model.predict(x_teste)
    return metricas("RIDGE",y_teste,y_pred)

# -----------------------------------------------
#  Bruno 
# -----------------------------------------------


def random_forest_treino(x_train, y_train, parametros=None):
    # Ordem no TXT: n_estimators, max_depth, min_samples_split, min_samples_leaf, max_features.
    if parametros is None:
        parametros = [80, 0, 2, 1, 1.0]
    if len(parametros) != 5:
        raise ValueError("Random Forest: informe os 5 valores na ordem indicada.")

    arvores, profundidade, min_divisao, min_folha, fracao = parametros
    modelo = RandomForestRegressor(
        n_estimators=arvores,
        max_depth=None if profundidade == 0 else profundidade,  # 0 = sem limite
        min_samples_split=min_divisao,
        min_samples_leaf=min_folha,
        max_features=float(fracao),  # 1 significa usar 100% dos atributos
        random_state=42,
        n_jobs=2,
    )
    return modelo.fit(x_train, y_train)


def random_forest_teste(x_teste, y_teste, modelo):
    previsoes = modelo.predict(x_teste)
    return metricas("RANDOM FOREST", y_teste, previsoes)


# -----------------------------------------------
# Leonardo
# -----------------------------------------------

def extra_trees_treino(x_train, y_train, parametros=None):
    p = [100, None, 2, 1, False, None]

    if parametros:
        p = list(parametros) + p[len(parametros):]

    et_model = ExtraTreesRegressor(
        random_state=42,
        n_estimators=p[0],
        max_depth=p[1],
        min_samples_split=p[2],
        min_samples_leaf=p[3],
        bootstrap= True if (int(p[4]) == 1) else False,
        max_features=p[5],
    )
    et_model.fit(x_train, y_train)
    return et_model

def extra_trees_teste(x_teste, y_teste, et_model):
    y_pred = et_model.predict(x_teste)
    return metricas("Extra Trees Regressor",y_teste,y_pred)

# -----------------------------------------------
# Enzo
# -----------------------------------------------
# LASSO-DatasetBoston
# Parametros: alpha, max_iter, grau_polinomial

def lasso_treino(x_train, y_train, parametros=None):
    p = [1.0, 1000, 1]

    if parametros:
        p = list(parametros) + p[len(parametros):]

    alpha, max_iter, grau = float(p[0]), int(p[1]), int(p[2])

    lasso_model = Pipeline([
        ("polinomial", PolynomialFeatures(degree=grau, include_bias=False)),
        ("padronizacao", StandardScaler()),
        ("lasso", Lasso(alpha=alpha, max_iter=max_iter, tol=0.0005)),
    ])

    lasso_model.fit(x_train, y_train)
    return lasso_model

def lasso_teste(x_teste, y_teste, lasso_model):
    y_pred = lasso_model.predict(x_teste)
    return metricas("LASSO", y_teste, y_pred)



# -----------------------------------------------
# Felipe Machado
# -----------------------------------------------

def adaboost_treino(x_train, y_train, parametros=None):
    p = [100, 0.5, 4, 0]

    if parametros:
        p = list(parametros) + p[len(parametros):]

    ada_model = AdaBoostRegressor(
        estimator=DecisionTreeRegressor(max_depth=int(p[2])),
        n_estimators=int(p[0]),
        learning_rate=p[1],
        random_state=int(p[3])
    )

    ada_model.fit(x_train, y_train)
    return ada_model

def adaboost_teste(x_teste, y_teste, ada_model):
    y_pred = ada_model.predict(x_teste)
    return metricas("ADABOOST", y_teste, y_pred)


# -----------------------------------------------
# Filipe Zuin
# -----------------------------------------------

def svr_treino(x_train, y_train, parametros=None):
    p = [1.0, 0.1, "scale"]

    if parametros:
        p = list(parametros) + p[len(parametros):]

    svr_model = SVR(
        C=float(p[0]),
        epsilon=float(p[1]),
        kernel="rbf",
        gamma=p[2] if p[2] == "scale" else float(p[2])
    )

    svr_model.fit(x_train, y_train)
    return svr_model


def svr_teste(x_teste, y_teste, svr_model):
    y_pred = svr_model.predict(x_teste)
    return metricas("SVR", y_teste, y_pred)



# -----------------------------------------------
# João Pedro
# -----------------------------------------------

def bagging_treino(x_train, y_train, config):
    bagging_model = BaggingRegressor(
        n_estimators=int(config["n_estimators"]),
        max_features=config["max_features"],
        random_state=42,
        n_jobs=-1
    )
    bagging_model.fit(x_train, y_train)
    return bagging_model

def bagging_teste(x_teste, y_teste, bagging_model):
    y_pred = bagging_model.predict(x_teste)
    return metricas("BAGGING",y_teste,y_pred)



# -----------------------------------------------
# Paulo
# -----------------------------------------------


def knn_treino(x_train, y_train, parametros=None):
    p = [5, 'uniform', 'auto', 30, 2, 'minkowski', 1]

    if parametros:
        p = list(parametros) + p[len(parametros):]

    knn_model = KNeighborsRegressor(
        n_neighbors=int(p[0]),
        weights=p[1],
        algorithm=p[2],
        leaf_size=int(p[3]),
        p=int(p[4]),
        metric=p[5],
        n_jobs=int(p[6])
    )

    knn_model.fit(x_train, y_train)
    return knn_model

def knn_teste(x_teste, y_teste, knn_model):
    y_pred = knn_model.predict(x_teste)
    return metricas("KNN", y_teste, y_pred)



# -----------------------------------------------
# Paulo
# -----------------------------------------------

def huber_regressor_treino(x_train, y_train, parametros=None):
    p = [1.35, 100, 0.0001, 0]

    if parametros:
        p = list(parametros) + p[len(parametros):]

    huber_model = HuberRegressor(
        epsilon=float(p[0]),
        max_iter=int(p[1]),
        alpha=float(p[2]),
    )

    if int(p[3]) == 1:
        modelo = Pipeline([
            ("poly", PolynomialFeatures(degree=2, include_bias=False)),
            ("scaler", StandardScaler()),
            ("huber", huber_model),
        ])
    else:
        modelo = huber_model

    modelo.fit(x_train, y_train)
    return modelo


def huber_regressor_teste(x_teste, y_teste, huber_model):
    y_pred = huber_model.predict(x_teste)
    return metricas("HUBER REGRESSOR", y_teste, y_pred)



#Vinicius Olv
def sgd_regressor_treino(x_train, y_train, parametros=None):
   
    p = [0.0001, 1000, 0.0001, 0.0005, 0, 4]

    if parametros:
        p = list(parametros) + p[len(parametros):]

    
    sgd_model = make_pipeline(
        PolynomialFeatures(degree=int(p[5]), include_bias=False),
        StandardScaler(),
        SGDRegressor(
            alpha=p[0],
            max_iter=int(p[1]),
            tol=p[2],
            eta0=p[3],
            random_state=int(p[4])
        )
    )

    sgd_model.fit(x_train, y_train)
    return sgd_model

def sgd_regressor_teste(x_teste, y_teste, sgd_model):
    y_pred = sgd_model.predict(x_teste)
    return metricas("SGD REGRESSOR", y_teste, y_pred)


