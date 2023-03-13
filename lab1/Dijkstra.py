from dimacs import loadWeightedGraph
from queue import PriorityQueue


def solve(f_name):
    n, L, sol = loadWeightedGraph(f_name)
    g = [[] for _ in range(n)]
    for a, b, w in L:
        g[a-1].append([b-1, w])
        g[b-1].append([a-1, w])

    pq = PriorityQueue()
    dist = [0 for _ in range(n)]
    visit = [False for _ in range(n)]
    dist[0] = max(c for a, b, c in L)
    pq.put((-dist[0], 0))

    while not pq.empty():
        d, v = pq.get()
        if v == 1:
            return -d, int(sol)
        if not visit[v]:
            for a, w in g[v]:
                w = min(w, -d)
                if dist[a] < w:
                    dist[a] = w
                    pq.put((-w, a))
            visit[v] = True

    return 0, int(sol)