from dimacs import *
from os import listdir
from os.path import isfile, join
from LexBFS import lex_bfs

def check_chordal(name):
    lex_order, g = lex_bfs(name)
    n = len(lex_order)
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
                if s != before and index[s] < index[v] and s not in g[before]:
                    return False
    return True


file_names = [f for f in listdir('chordal') if isfile(join('chordal', f))]
for f in file_names:
    sol = readSolution('chordal/' + f)
    print(check_chordal('chordal/' + f), sol)
