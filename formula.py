import numpy as np
import matplotlib.pyplot as plt


def p_1(alpha):
    # This comes from Equation 4
    return (alpha - 2 * alpha ** 2) / (2 * alpha ** 3 - 4 * alpha ** 2 + 1)

def p_0(alpha):
    # This comes from Equation 2
    return p_1(alpha) / alpha

def p_0prime(alpha):
    # This comes from Equation 3
    return p_1(alpha) * (1 - alpha)

def p_k(alpha, k):
    # This comes from Equation 5
    return p_1(alpha) * (alpha / (1 - alpha)) ** (k - 1)

def p_gt2(alpha):
    # This comes from Equation 5
    # and infinite sum of geometric series formula which is "a / (1 - r)", in which
    a = p_k(alpha, 3)           # p_3, the initial term
    r = alpha / (1 - alpha)     # the common ratio
    return a / (1 - r)

def r_others(alpha, gamma):
    # This comes from Equation 6
    return p_0prime(alpha) * gamma * (1 - alpha) * 1 + p_0prime(alpha) * (1 - gamma) * (1 - alpha) * 2 + p_0(alpha) * (1 - alpha) * 1

def r_selfish(alpha, gamma):
    # This comes from Equation
    return p_0prime(alpha) * alpha * 2 + p_0prime(alpha) * gamma * (1 - alpha) * 1 + p_k(alpha, 2) * (1 - alpha) * 2 + p_gt2(alpha) * (1 - alpha) * 1

def r_total(alpha, gamma):
    # This comes from Equation 8
    return (alpha * (1 - alpha) ** 2 * (4 * alpha + gamma * (1 - 2 * alpha)) - alpha ** 3) /\
            (1 - alpha * (1 + (2 - alpha) * alpha))

gamma = 0

# plt.figure(figsize=(12, 4))
#
# X = np.linspace(0.001, 0.499, 499)
# plt.plot(X, X)
# for g in [0]:#, .5, 1): #(0, .2, .4, .6, .8, 1):
#     # g = gamma
#     Y_selfish = np.array([r_selfish(a, g) for a in X])
#     Y_others = np.array([r_others(a, g) for a in X])
#     Y_total = Y_selfish + Y_others
#     # plt.plot(X, Y_others, label="others".format(g))
#     plt.plot(X, Y_selfish, label="selfish".format(g))
#     # plt.plot(X, 1 - X)
#     # plt.plot(X, 1 + 0 * X)
#     # plt.plot(X, Y_others / Y_total, label="others after".format(g))
#     plt.plot(X, Y_selfish / Y_total, label="selfish after".format(g))
#     plt.plot(X, [r_total(a, g) for a in X])
#     # plt.plot(X, Y_total)
#
# plt.xlim(0, 0.5)
# plt.ylim(0, 1)
# plt.legend()
#
# plt.show()
#
#
# plt.figure(figsize=(8, 8))
# X = np.linspace(0, 0.5, 501)
#
# plt.subplot(221)
# plt.title("Numerical, from formulas 2 to 7")
# plt.xlabel("Pool size")
# plt.ylabel("Relative pool revenue")
# plt.plot(X, X, label="Honest mining", color="#777777")
#
# plt.subplot(222)
# plt.title("From formula 8")
# plt.xlabel("Pool size")
# plt.ylabel("Relative pool revenue")
# plt.plot(X, X, label="Honest mining", color="#777777")
#
#
# line_styles = {0: 'r--', 0.5: 'g-', 1: 'b-'}
# for g in (0, .5, 1):
#     Y_selfish = np.array([r_selfish(a, g) for a in X])
#     Y_others  = np.array([r_others(a, g)  for a in X])
#     Y_total = Y_selfish + Y_others
#
#     Y_numeric = Y_selfish / Y_total
#     Y_formula = [r_total(a, g) for a in X]
#
#     plt.subplot(221)
#     plt.plot(X, Y_numeric, line_styles[g], label="γ = {}".format(g))
#
#     plt.subplot(222)
#     plt.plot(X, Y_formula, line_styles[g], label="γ = {}".format(g))
#
#     plt.subplot(223)
#     plt.plot(X, Y_formula - Y_numeric, line_styles[g], label="γ = {}".format(g))
#
#
# plt.subplot(221)
# plt.xlim(0, 0.5)
# plt.ylim(0, 1.0)
# plt.legend()
#
# plt.subplot(222)
# plt.xlim(0, 0.5)
# plt.ylim(0, 1.0)
# plt.legend()
#
# plt.subplot(223)
# plt.xlim(0, 0.5)
# plt.ylim(-0.001, 0.001)
# plt.legend()
#
# plt.show()

"""
alpha = .49
gamma = .00

T = 2016 / 6

X = np.linspace(0, 7000, 701)
Y = np.zeros((701))

for t in range(701):
    r_pool = r_selfish(alpha, gamma)
    r_total = r_pool + r_others(alpha, gamma)
    if X[t] < T:
        Y[t] = r_pool * X[t]
    else:
        Y[t] = r_pool * T + r_pool / r_total * (X[t] - T)

G = (Y - X * alpha) / X * 100

for i in range(len(X)):
    if G[i] >= 0:
        X_0 = X[i]
        break

try:
    print(X_0)
except:
    print("NA")

plt.figure(figsize=(6, 4))
plt.plot(X, G, "r", label="alpha = {:.2f}".format(alpha))
# plt.plot(X, X * alpha)
plt.plot([0, max(X)], [0, 0], "k--")
plt.ylim(-15, 15)
plt.legend()
plt.show()
#"""

def get_X_and_G(alpha, gamma=0):
    T = 2016 / 6

    X = np.linspace(0, 7000, 701)
    Y = np.zeros((701))

    r_pool = r_selfish(alpha, gamma)
    r_total = r_pool + r_others(alpha, gamma)
    Tt = T / r_total
    for t in range(701):
        if X[t] < Tt:
            Y[t] = r_pool * X[t]
        else:
            Y[t] = r_pool * Tt + r_pool / r_total * (X[t] - Tt)

    G = (Y - X * alpha) / X * 100

    for i in range(len(X)):
        if G[i] >= 0:
            X_0 = X[i]
            break

    try:
        print(alpha, X_0)
    except:
        print("NA")

    return X, G


for i in range(33, 50):
    alpha = i / 100
    get_X_and_G(alpha, 0)
