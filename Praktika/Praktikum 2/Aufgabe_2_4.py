import numpy as np
from sklearn.linear_model import LinearRegression
import Aufgabe_2_2 as aufgabe2_2

X_sklearn = aufgabe2_2.x.reshape(-1, 1)

reg = LinearRegression()
reg.fit(X_sklearn, aufgabe2_2.y)

print(f"Unsere Implementierung (Beta_1): {aufgabe2_2.beta[1]}")
print(f"Scikit-Learn (Coef):             {reg.coef_[0]}")