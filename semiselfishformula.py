import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import rc


def r_selfish(a, g):
    return (a * ((1 - a) ** 2) * (4 * a + g * (1 - 2 * a)) - a ** 3) / (1 - a * (1 + (2 - a) * a))

def r_semi_selfish(a, g):
    return (a * (a * (a * (2 * a - 5) + 4) - (a - 1) ** 3 * g)) / ((a - 1) * a ** 2 + 1)


"""
plt.figure(figsize=(12, 4))

alpha = np.linspace(0, 0.5, 501)
plt.plot(alpha, alpha, 'k--')

Y_selfish = np.array([r_selfish(a, a) for a in alpha])
plt.plot(alpha, Y_selfish, label="selfish")

g = 0
Y_semi_selfish = np.array([r_semi_selfish(a, g) for a in alpha])
plt.plot(alpha, Y_semi_selfish, label="semi-selfish (gamma={})".format(g))

# g = .25
# Y_semi_selfish = np.array([r_semi_selfish(a, g) for a in alpha])
# plt.plot(alpha, Y_semi_selfish, label="semi-selfish (gamma={})".format(g))

g = .5
Y_semi_selfish = np.array([r_semi_selfish(a, g) for a in alpha])
plt.plot(alpha, Y_semi_selfish, label="semi-selfish (gamma={})".format(g))


Y_semi_selfish = np.array([r_semi_selfish(a, a) for a in alpha])
plt.plot(alpha, Y_semi_selfish, label="semi-selfish (gamma={})".format("alpha"))


plt.plot([0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.37, 0.40, 0.42, 0.45, 0.47, 0.48, 0.49, 0.50], [0.009, 0.033, 0.069, 0.115, 0.172, 0.237, 0.315, 0.351, 0.410, 0.454, 0.541, 0.625, 0.680, 0.784, 0.912], label="simulation")


plt.xlim(0, 0.5)
plt.ylim(0, 1)
plt.legend()
plt.show()
"""

fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122, projection='3d')

G = np.arange(0, 1.0, 0.1)
len_G = np.shape(G)[0]
A = np.arange(0, 0.5, .02)
len_A = np.shape(A)[0]

X, Y = np.meshgrid(G, A)

SS = np.ones((len_A, len_G))
S = np.ones((len_A, len_G))

for i in range(len_A):
    for j in range(len_G):
        S[i, j] = r_selfish(A[i], G[j])
        SS[i, j] = r_semi_selfish(A[i], G[j])


ax.plot_surface(X, Y, S, rstride=1, cstride=1, cmap='plasma', edgecolor='none')
ax.plot_surface(X, Y, SS, rstride=1, cstride=1, cmap='plasma', edgecolor='none')

plt.show()

