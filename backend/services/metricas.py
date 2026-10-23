import numpy as np
from sklearn import metrics as metrics

def metricas(texto,y_teste,y_pred):
    mae = metrics.mean_absolute_error(y_teste, y_pred)
    mse = metrics.mean_squared_error(y_teste, y_pred)
    rmse = np.sqrt(mse)
    r2 = metrics.r2_score(y_teste, y_pred)
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