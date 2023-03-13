from dimacs import loadWeightedGraph


class Node:
    def __init__(self):
        self.parent = self
        self.rank = 1


def find(x):
    if x.parent != x:
        x.parent = find(x.parent)
    return x.parent


def union(a, b):
    a = find(a)
    b = find(b)
    if a != b:
        if a.rank > b.rank:
            b.parent = a
        else:
            a.parent = b
            b.rank += (a.rank == b.rank)


def solve(f_name):
    n, L, sol = loadWeightedGraph(f_name)
    L.sort(key = lambda x: -x[2])
    nodes = [Node() for _ in range(n)]
    for a, b, c in L:
        union(nodes[a-1], nodes[b-1])
        if find(nodes[0]) == find(nodes[1]):
            return c, sol
    return 0, sol
