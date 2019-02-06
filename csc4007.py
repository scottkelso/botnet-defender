import numpy as np
from numpy.linalg import inv, pinv

a = np.array([[1, 2], [3, 4]])
b = np.array([[1, 0], [0, 1]])
c = np.array([[1, 2, -3], [2, -1, 2], [3, 2, 4]])

# Inverse of a: A^(-1)
inv(a)
# Estimates inverse when one doesn't exist
pinv(a)

# Matrix Multiplication
np.matmul(a, b)

# Transpose: A^T
a.transpose()

# Matrix Determinant
np.linalg.det(c)
