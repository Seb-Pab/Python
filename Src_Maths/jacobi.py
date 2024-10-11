from joblib import Parallel, delayed
import numpy as np

# La matrice A contient
# notre système.
A = [[2, 1,    1, -1],
     [0, 1.5, -1,  0],
     [0, 0,    3, -1],
     [0, 0,    0,  1]]

# la matrice colonne B
# contient le terme de droite.
B = [0, 0, 2, 43]

# La fonction Jacobi
# calcule une solution approchée
# de notre systeme
def jacobi(A, B, maxIter):
    nligsA, ncolsA = len(A), len(A[0])
    X = [0.0] * ncolsA

    for j in range(0, maxIter):
        # Notez la seule différence avec la méthode de Gauss-Seidel
        # Les nouvelles valeurs de X sont calculées depuis celles de l'itération précédente.
        X_c = X.copy()
        for i in range(0, ncolsA):
            X_c[i] = 0
            X[i] = (B[i] - np.dot([col for col in A[i]], X_c)) / A[i][i]
    return X

def parallel_jacobi(A, B, maxIter):
    nligsA, ncolsA = len(A), len(A[0])
    X = [0.0] * ncolsA

    def update_x_i(A, B, X, i):
        X[i] = 0
        return (B[i] - np.dot([col for col in A[i]], X)) / A[i][i]

    for j in range(0, maxIter):
        # Ici, la boucle a été transformée en calculs indépendants
        # exécutés en parallèle.
        X = Parallel(n_jobs=8)(delayed(update_x_i)(A, B, X.copy(), i) for i in range(0, ncolsA))

    return X

# Avec une seule iteration
# on est loin du résultat.
print(jacobi(A, B, 1))
# > [0.0, 0.0, 0.666, 43.0]
# Avec une de plus
# on se rapproche.
print(jacobi(A, B, 2))
# > [21.166666666666668, 0.4444444444444444, 15.0, 43.0]

# et deux de plus
# suffisent à trouver la
# solution exacte.
print(jacobi(A, B, 4))
# > [9.0, 10.0, 15.0, 43.0]


# Même chose avec la version parallélisée.
print(parallel_jacobi(A, B, 4))
# > [9.0, 10.0, 15.0, 43.0] - le résultat est le même.
