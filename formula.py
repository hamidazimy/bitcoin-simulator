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
    # Denominator of Equation 8
    return r_selfish(alpha, gamma) + r_others(alpha, gamma)

def R_selfish(alpha, gamma):
    # This comes from Equation 8
    return (alpha * (1 - alpha) ** 2 * (4 * alpha + gamma * (1 - 2 * alpha)) - alpha ** 3) /\
            (1 - alpha * (1 + (2 - alpha) * alpha))

def R_selfish_t(alpha, gamma=0, MAX_HEIGHT=4096):
    T = 2016 / 6
    MAX_T = MAX_HEIGHT / 6
    N = 1001
    t = np.linspace(0, MAX_T, N)

    r_pool = r_selfish(alpha, gamma)
    r_total = r_pool + r_others(alpha, gamma)
    r_total_ = 1 / r_total
    # print(r_total, r_total_)
    # print(r_total_ - 1)
    # print(r_pool)
    T_1 = T / r_total
    R_pool = r_pool / r_total
    L = (R_pool - r_pool) * T_1 * 6

    print(f"alpha  = {alpha}")
    print(f"r_pool = {r_pool}")
    print(f"R_pool = {R_pool}")

    Rt = np.ones((N,))
    for i in range(1, N):
        if t[i] < T_1:
            Rt[i] = r_pool * t[i] * 6
        else:
            Rt[i] = R_pool * t[i] * 6 - L

    print(f" t[0]: { t[1]},  t[-1]: { t[-1]}")
    print(f"Rt[0]: {Rt[1]}, Rt[-1]: {Rt[-1]}")

    return t, Rt


def get_t_and_Gt(alpha, gamma=0, MAX_HEIGHT=4096):
    T = 2016 / 6

    MAX_T = MAX_HEIGHT / 6

    N = 1001

    t = np.linspace(0, MAX_T, N)
    # Y = np.zeros((N))

    r_pool = r_selfish(alpha, gamma)
    r_total = r_pool + r_others(alpha, gamma)
    r_total_ = 1 / r_total
    # print(r_total, r_total_)
    # print(r_total_ - 1)
    # print(r_pool)
    T_1 = T / r_total
    R_pool = r_pool / r_total

    Gt = np.ones((N,))# * (R_pool - alpha)

    t, Rt = R_selfish_t(alpha, gamma, MAX_HEIGHT)
    Gt = (Rt - alpha * 6 * t) / (6 * t)

    Gt[0] = R_pool

    print(Gt[10])

    # Gt = np.ones((N)) * ((R_pool - alpha) * 100)

    for i in range(1, N):
        # Gt[i] -= (r_pool * (r_total_ - 1) * T) / t[i]
        if t[i] < T_1:
            Gt[i] = (r_pool - alpha)
        else:
            Gt[i] = (R_pool - alpha) - (R_pool - r_pool) * T_1 / t[i]

    # Gt = (Y - X * alpha) / X * 100

    # for i in range(len(X)):
    #     if Gt[i] >= 0:
    #         X_0 = X[i]
    #         break
    #
    # try:
    #     print(alpha, X_0)
    # except:
    #     print("NA")

    Gt *= 1 / 6
    return t, Gt


def t_breakeven(alpha, gamma=0):
    r_s = r_selfish(alpha, gamma)
    r_o = r_others(alpha, gamma)
    r_t = r_s + r_o
    R_s = r_s / r_t
    return (R_s - r_s) * r_t / (R_s - alpha) * (2016 / 6)

def plot_G(alpha):
    t, Gt = get_t_and_Gt(alpha, 0, 40960)

    plt.figure(figsize=(6, 4))
    plt.plot(t[1:], Gt[1:], "r", label="alpha = {:.2f}".format(alpha))
    # plt.plot(X, X * alpha)
    plt.plot([0, max(t)], [0, 0], "k--")
    plt.plot([0, max(t)], [Gt[0], Gt[0]], "y--")
    plt.ylim(-.015, .015)
    plt.legend()
    plt.show()


def q_(q, l):
    return (q * (1 - q) ** 2 * (4 * q + l * (1 - 2 * q)) - q ** 3) / (1 - q * (1 + q * (2 - q)))

def Edelta(p, q):
    return (p - q + p * q * (p - q) + p * q) / (p ** 2 * q + p - q)

def Et0(p, q, l, n0, t0):
    return (q_(q, l) * (Edelta(p, q) - 1)) / (q_(q, l) - q) * (n0 * t0)

def plot_grunspan2018profitability_Fig2():
    l = .5
    Q = np.array([x / 1000 for x in range(270, 499)])
    P = 1 - Q
    Y = np.array([Et0(P[i], Q[i], l, 2016, 1) for i in range(len(Q))]) / 7 / 24 / 6
    # Y = [Edelta(P[i], Q[i]) for i in range(len(Q))]
    # Y = [q_(Q[i], .5) for i in range(len(Q))]
    # print([f"{y:.1f}" for y in Y])

    plt.figure(figsize=(6, 4))
    plt.plot(Q, Y, "r")
    plt.xlabel("q")
    plt.ylabel("Weeks")
    plt.ylim([0, 14])
    # plt.show()

def plot_breakeven():
    gamma = .5
    alpha = np.array([x / 1000 for x in range(270, 499)])
    # l = gamma
    # Q = alpha
    # P = 1 - Q
    # Y = np.array([Et0(P[i], Q[i], gamma, 2016, 1) for i in range(len(Q))]) / 7 / 24 / 6
    breakeven = np.array([t_breakeven(alpha[i], gamma) for i in range(len(alpha))]) / 7 / 24

    plt.figure(figsize=(6, 4))
    plt.plot(alpha, breakeven, "b")
    # plt.plot(Q, Y, "r")
    plt.show()


if __name__ == "__main__":
    alpha = .35
    gamma = .5
    # plot_grunspan2018profitability_Fig2()
    # plot_breakeven()
    plot_G(alpha)

