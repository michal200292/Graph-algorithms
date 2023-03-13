from dimacs import *
from math import inf
from queue import PriorityQueue


def mergeVertices(g, m, x, y):
    new_g = [{} for _ in range(m - 1)]
    mapping = [i for i in range(m)]
    cur = 0
    for i in range(m):
        if i != x and i != y:
            mapping[i] = cur
            cur += 1

    for i in range(m):
        if i != x and i != y:
            v = mapping[i]
            for s in g[i]:
                if s != x and s != y:
                    new_g[v][mapping[s]] = g[i][s]
                else:
                    if m - 2 not in new_g[v]:
                        new_g[v][m - 2] = g[i][s]
                        new_g[m - 2][v] = g[s][i]
                    else:
                        new_g[v][m - 2] += g[i][s]
                        new_g[m - 2][v] += g[i][s]
    return new_g


def minimumCutPhase(g, n):
    visit = [False for _ in range(n)]
    dist = [0 for _ in range(n)]
    added = []
    q = PriorityQueue()
    q.put((0, 0))
    last = 0
    while not q.empty():
        l, v = q.get()
        if not visit[v]:
            added.append(v)
            last = l
            for s in g[v]:
                if not visit[s]:
                    dist[s] -= g[v][s]
                    q.put((dist[s], s))
            visit[v] = True

    return -last, added[-2], added[-1]


def solve(f_name):
    n, edges = loadWeightedGraph(f_name)
    g = [{} for _ in range(n)]
    for a, b, c in edges:
        g[a - 1][b - 1] = c
        g[b - 1][a - 1] = c

    ans = inf
    for _ in range(n - 1):
        cut, x, y = minimumCutPhase(g, n)
        ans = min(ans, cut)
        g = mergeVertices(g, n, x, y)
        n -= 1
    return ans


print(solve('clique100'))

