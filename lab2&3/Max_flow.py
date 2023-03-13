from tree import generate
from math import inf
from collections import deque


def bfs(g, res, parent):
    visit = [False for _ in range(len(parent))]
    visit[0] = True
    d = deque()
    d.append(0)
    while d:
        v = d.popleft()
        for s in g[v]:
            if not visit[s] and res[v][s]:
                visit[s] = True
                parent[s] = (v, min(parent[v][1], res[v][s]))
                d.append(s)
    return parent[-1][1]


def update(res, parent, x):
    v = len(parent) - 1
    while parent[v][0] is not None:
        res[parent[v][0]][v] -= x
        res[v][parent[v][0]] += x
        v = parent[v][0]


def max_f():
    res, n = generate(10, 30)
    for row in res:
        for r in row:
            print(r, end=",")
        print()
    g = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if res[i][j] or res[j][i]:
                g[i].append(j)

    f = 0
    parent = [(None, 0) for _ in range(n)]
    parent[0] = (None, inf)
    while x := bfs(g, res, parent):
        f += x
        update(res, parent, x)
        parent = [(None, 0) for _ in range(n)]
        parent[0] = (None, inf)


    return f


print(max_f())