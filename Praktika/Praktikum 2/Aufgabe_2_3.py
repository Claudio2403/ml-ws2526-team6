import numpy as np
import Aufgabe_2_2 as aufgabe2_2

def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    
    error = y_true - y_pred
    squared_error = error ** 2
    mse_value = np.mean(squared_error)

    return mse_value

mse_result = mse(aufgabe2_2.y, aufgabe2_2.y_hat)
print(f"Der MSE (Mean Squared Error) beträgt: {mse_result}")
