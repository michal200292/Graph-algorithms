from data import runtests


def change_interval(key, vertices, vertices_to_swap, pointers, intervals, interval_info):
    m = len(vertices_to_swap)
    left, right = intervals[key][0], intervals[key][1]
    if right - left + 1 == m:
        return

    new_left = right - m + 1
    k = len(intervals)
    intervals[key][1] = new_left - 1
    intervals.append([new_left, right])

    i = right
    for j in range(m):
        v = vertices_to_swap[j]
        pos = pointers[v]
        s = vertices[i]
        pointers[v], pointers[s] = i, pos
        vertices[i], vertices[pos] = vertices[pos], vertices[i]
        interval_info[v] = k
        i -= 1


def lex_bfs(g, n):
    vertices = [n - i - 1 for i in range(n)]
    pointers = [n - i - 1 for i in range(n)]
    intervals = [[0, n - 1]]
    interval_info = [0 for _ in range(n)]
    lex_order = []

    change = [[] for _ in range(2*n)]
    used = [False for _ in range(n)]
    for _ in range(n):
        v = vertices.pop()
        lex_order.append(v)
        intervals[interval_info[v]][1] -= 1
        tak = []
        for x in g[v]:
            if not used[x]:
                if not change[interval_info[x]]:
                    tak.append(interval_info[x])
                change[interval_info[x]].append(x)

        for key in tak:
            change_interval(key, vertices, change[key], pointers, intervals, interval_info)
            change[key] = []
        used[v] = True
    return lex_order


def check_correct(vertices, n, g, clique_size):
    for v in range(n):
        if not vertices[v]:
            count = 0
            for s in g[v]:
                if not vertices[s]:
                    count += 1
            if count != clique_size - 1:
                return False
    return True


def independent(vertices, g, v, x):
    for s in g[v]:
        if s != x and vertices[s]:
            return False
    return True


def edge_case_correction(vertices, g, n, clique_size):
    v = -1
    for i in range(n):
        if vertices[i] and len(g[i]) == clique_size:
            v = i
    if v == -1:
        return

    x = -1
    for s in g[v]:
        if len(g[s]) < clique_size and independent(vertices, g, s, v) and (x == -1 or len(g[s]) < len(g[x])):
            x = s

    if x == -1:
        return
    vertices[v], vertices[x] = False, True


def my_solve(n, channels):
    if len(channels) == 0:
        return 1
    if len(channels) == (n*(n - 1) // 2):
        return n - 1

    g = [[] for _ in range(n)]
    for a, b in channels:
        g[a - 1].append(b - 1)
        g[b - 1].append(a - 1)

    lex_order = lex_bfs(g, n)
    vertices = [False for _ in range(n)]
    count = 0
    for i in range(n - 1, -1, -1):
        v = lex_order[i]
        for s in g[v]:
            if vertices[s]:
                break
        else:
            vertices[v] = True
            count += 1

    edge_case_correction(vertices, g, n, n - count)
    if check_correct(vertices, n, g, n - count):
        return n - count
    return None


runtests(my_solve)
