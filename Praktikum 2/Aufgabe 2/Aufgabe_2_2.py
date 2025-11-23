import numpy as np

x = np.array([2.0, 3.0, 5.0, 7.0, 9.0])
y = np.array([1.0, 2.0, 2.5, 2.5, 4.0])

X = np.c_[np.ones_like(x), x]

def normal_equation(X, y):
    beta = np.linalg.inv(X.T @ X) @ X.T @ y
    return beta

def predict(X, beta):
    y_hat = X @ beta
    return y_hat

if __name__ == "__main__":
    beta = normal_equation(X, y)
    y_hat = predict(X, beta)
    print("Geschätzte Koeffizienten (beta):", [float(v) for v in beta])
    print("Vorhergesagte Werte (y_hat):", [float(v) for v in y_hat])

    x_test = np.array([4.0, 6.5, 11.0])
    X_test = np.c_[np.ones_like(x_test), x_test]
    y_test_hat = predict(X_test, beta)

    print("Test-x-Werte:", [float(v) for v in x_test])
    print("Vorhersagen für Testwerte:", [float(v) for v in y_test_hat])