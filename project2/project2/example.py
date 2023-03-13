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
    return lex_order


def check_correct(vertices, n, g, g_sets):
    rest = set([i for i in range(n) if i not in vertices])
    m = len(rest)
    for v in rest:
        count = 0
        for s in g[v]:
            if s in rest:
                count += 1
        if count < m - 1:
            return False
    return True


def my_solve(n, channels):
    if not channels:
        return 1

    g = [[] for _ in range(n)]
    for a, b in channels:
        g[a - 1].append(b - 1)
        g[b - 1].append(a - 1)

    lex_order = lex_bfs(g, n)
    g_sets = [set(g[i]) for i in range(n)]

    index = [0 for _ in range(n)]
    for i in range(n):
        index[lex_order[i]] = i

    pred = [0 for _ in range(n)]
    for i in range(n):
        for s in g[i]:
            if index[i] < index[s]:
                pred[s] = max(pred[s], index[i])

    for i in range(1, n):
        v = lex_order[i]
        before = lex_order[pred[v]]
        if before != -1:
            for s in g[v]:
                if s != before and index[s] < index[v] and s not in g_sets[before]:
                    return None

    vertices = set()
    count = 0
    for i in range(n - 1, -1, -1):
        v = lex_order[i]
        for s in g[v]:
            if s in vertices:
                break
        else:
            vertices.add(v)
            count += 1

    if check_correct(vertices, n, g, g_sets):
        return n - count
    return None


runtests(my_solve)
