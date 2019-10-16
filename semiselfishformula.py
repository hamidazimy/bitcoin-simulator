import numpy as np
import matplotlib.pyplot as plt


def r_selfish(a, g):
    return (a * ((1 - a) ** 2) * (4 * a + g * (1 - 2 * a)) - a ** 3) / (1 - a * (1 + (2 - a) * a))

def r_semi_selfish(a, g):
    return (a * (a * (a * (2 * a - 5) + 4) - (a - 1) ** 3 * g)) / ((a - 1) * a ** 2 + 1)


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



plt.xlim(0, 0.5)
plt.ylim(0, 1)
plt.legend()
plt.show()


