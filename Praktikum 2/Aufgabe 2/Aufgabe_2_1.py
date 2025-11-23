import numpy as np

x = np.array([2.0, 3.0, 5.0, 7.0, 9.0])
y = np.array([1.0, 2.0, 2.5, 2.5, 4.0])

X = np.c_[np.ones_like(x), x]

def normal_equation(X, y):
    beta = np.linalg.inv(X.T @ X) @ X.T @ y
    return beta.squeeze()

if __name__ == "__main__":
    beta = normal_equation(X, y)
    print("Koeffizienten:", beta)