from dimacs import *
from os import listdir
from os.path import isfile, join

def checkLexBFS(G, vs):
    n = len(G)
    pi = [None] * n
    for i, v in enumerate(vs):
        pi[v] = i

    for i in range(n - 1):
        for j in range(i + 1, n - 1):
            Ni = G[vs[i]]
            Nj = G[vs[j]]

            verts = [pi[v] for v in Nj - Ni if pi[v] < i]
            if verts:
                viable = [pi[v] for v in Ni - Nj]
                if not viable or min(verts) <= min(viable):
                    return False
    return True

def convert_graph(n, E):
    g = [set() for _ in range(n)]
    for a, b, _ in E:
        g[a - 1].add(b - 1)
        g[b - 1].add(a - 1)
    return g


def lex_bfs(name):
    n, E = loadWeightedGraph(name)
    g = convert_graph(n, E)
    sets = [set()]
    for i in range(n):
        sets[0].add(i)

    lex_ord = []
    for i in range(n):
        v = sets[-1].pop()
        lex_ord.append(v)
        if not sets[-1]:
            sets.pop()
        new_sets = []
        for s in sets:
            left = set()
            right = set()
            for x in s:
                if x in g[v]:
                    right.add(x)
                else:
                    left.add(x)
            if left:
                new_sets.append(left)
            if right:
                new_sets.append(right)
        sets = new_sets
    return lex_ord, g


def change_interval(key, vertices, vertices_to_swap, pointers, intervals, interval_info):
    m = len(vertices_to_swap)
    left, right = intervals[key][0], intervals[key][1]
    if right - left + 1 == m:
        return
    i = right
    for j in range(m):
        v = vertices_to_swap[j]
        pos = pointers[v]
        s = vertices[i]
        pointers[v], pointers[s] = i, pos
        vertices[i], vertices[pos] = vertices[pos], vertices[i]
        i -= 1
    new_left = right - m + 1
    k = len(intervals)
    intervals[key][1] = new_left - 1
    intervals.append([new_left, right])
    for v in vertices_to_swap:
        interval_info[v] = k


def linear_lex_bfs(name):
    n, E = loadWeightedGraph(name)
    tak = convert_graph(n, E)
    g = [[] for _ in range(n)]
    for a, b, _ in E:
        g[a - 1].append(b - 1)
        g[b - 1].append(a - 1)

    vertices = [n - i - 1 for i in range(n)]
    pointers = [0 for _ in range(n)]
    for i, v in enumerate(vertices):
        pointers[v] = i
    intervals = [[0, n - 1]]
    interval_info = [0 for _ in range(n)]
    lex_order = []
    used = [False for _ in range(n)]
    for _ in range(n):
        v = vertices.pop()
        lex_order.append(v)
        intervals[interval_info[v]][1] -= 1
        change = {}
        for x in g[v]:
            if not used[x]:
                if interval_info[x] in change:
                    change[interval_info[x]].append(x)
                else:
                    change[interval_info[x]] = [x]
        for key in change:
            change_interval(key, vertices, change[key], pointers, intervals, interval_info)
        used[v] = True

    return checkLexBFS(tak, lex_order)


file_names = [f for f in listdir('chordal') if isfile(join('chordal', f))]
for f in file_names:
    print(linear_lex_bfs('chordal/' + f))

