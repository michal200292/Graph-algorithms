from dimacs import *
from os import listdir
from os.path import isfile, join
from LexBFS import lex_bfs


def graph_coloring(name):
    lex_order, g = lex_bfs(name)
    n = len(lex_order)
    color = [-1 for _ in range(n)]
    visit = [False for _ in range(n)]
    for x in lex_order:
        colors = set()
        for s in g[x]:
            if visit[s]:
                colors.add(color[s])
        mini = n
        if 0 not in colors:
            color[x] = 0
        else:
            for c in colors:
                if c + 1 not in colors:
                    mini = min(mini, c + 1)
            color[x] = mini
        visit[x] = True
    return max(color) + 1


file_names = [f for f in listdir('coloring') if isfile(join('coloring', f))]

for f in file_names:
    sol = readSolution('coloring/' + f)
    print(graph_coloring('coloring/' + f), sol)
