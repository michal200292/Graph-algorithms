from dimacs import loadWeightedGraph
from collections import deque


def path(weight, g, n):
    visit = [False for _ in range(n)]
    d = deque()
    visit[0] = True
    d.append(0)
    while d:
        v = d.popleft()
        for a, w in g[v]:
            if not visit[a] and w >= weight:
                if a == 1:
                    return True
                visit[a] = True
                d.append(a)
    return False


def solve(f_name):
    n, L, sol = loadWeightedGraph(f_name)
    g = [[] for _ in range(n)]
    for a, b, w in L:
        g[a-1].append([b-1, w])
        g[b-1].append([a-1, w])

    L.sort(key=lambda x: x[2])
    l, r = 0, len(L) - 1
    while l <= r:
        s = (l + r) // 2
        if path(L[s][2], g, n):
            l = s + 1
        else:
            r = s - 1

    return L[r][2], sol

