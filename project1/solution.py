from data import runtests
from math import inf


def greedy_sol(N, K, base, tab):
    cost = []
    for i in range(N):
        cost.append(tab[i][0] + base[i][0])
        for j in range(1, len(tab[i])):
            cost.append((tab[i][j] + base[i][j] - base[i][j - 1]))
    return sum(sorted(cost)[:K])

def my_solve(N, M, K, base, wages, eq_cost):
    dp = [[inf for _ in range(K + 1)] for _ in range(N)]
    tab = [[] for _ in range(N)]
    for i in range(N):
        tab[i] = sorted([wages[i][j][1] + eq_cost[wages[i][j][0] - 1] for j in range(len(wages[i]))])
        tab[i] = tab[i][:min(len(wages[i]), len(base[i]))]

    greedy = True
    for i in range(N):
        if len(base[i]) and len(tab[i]) > 1:
            if base[i][0] + tab[i][0] > base[i][1] - base[i][0] + tab[i][1]:
                greedy = False
            for j in range(2, min(len(base[i]), len(wages[i]))):
                if base[i][j] - base[i][j - 1] + tab[i][j] < base[i][j-1] - base[i][j - 2] + tab[i][j-1]:
                    greedy = False
    if greedy:
        return greedy_sol(N, K, base, tab)

    dp[0][0] = 0
    suma = 0
    for j in range(1, min(K + 1, len(tab[0]) + 1)):
        suma += tab[0][j - 1]
        dp[0][j] = suma + base[0][j - 1]

    pref = len(tab[0])
    for i in range(1, N):
        pref += len(tab[i])
        dp[i][0] = 0
        for j in range(1, min(K + 1, pref + 1)):
            dp[i][j] = dp[i - 1][j]
            suma = 0
            for k in range(1, min(j + 1, len(tab[i]) + 1)):
                suma += tab[i][k - 1]
                dp[i][j] = min(dp[i][j], base[i][k-1] + suma + dp[i-1][j - k])

    return dp[-1][-1]


runtests(my_solve)
