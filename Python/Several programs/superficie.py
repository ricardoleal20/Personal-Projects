import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as sp

# Dipole charge (C), Permittivity of free space (F.m-1)
q = 1.5e-20
eps0=sp.epsilon_0
# Dipole +q, -q distance (m) and a convenient combination of parameters
d = 2.e-12
k = 1/4/np.pi/eps0 * q * d

# Cartesian axis system with origin at the dipole (m)
X = np.linspace(-1e-12, 1e-12, 1000)
Y = X.copy()
X, Y = np.meshgrid(X, Y)

# Dipole electrostatic potential (V), using point dipole approximation
Phi = k * X / np.hypot(X, Y)**3

fig = plt.figure()
plt.title('Superficies equipotenciales para el problema 1.')
ax = fig.add_subplot(111)
# Draw contours at values of Phi given by levels
levels = np.array([10**pw for pw in np.linspace(0,5,20)])
levels = sorted(list(-levels) + list(levels))
# Monochrome plot of potential
ax.contour(X, Y, Phi, levels=levels, colors='k', linewidths=2)
plt.grid()
plt.show()