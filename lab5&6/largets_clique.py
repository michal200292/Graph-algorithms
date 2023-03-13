from dimacs import *
from os import listdir
from os.path import isfile, join
from LexBFS import lex_bfs


def max_clique(name):
    lex_order, g = lex_bfs(name)
    n = len(lex_order)
    visit = [False for _ in range(n)]
    ans = 1
    for x in lex_order:
        count = 1
        for s in g[x]:
            if visit[s]:
                count += 1
        ans = max(ans, count)
        visit[x] = True
    return ans


file_names = [f for f in listdir('maxclique') if isfile(join('maxclique', f))]

for f in file_names:
    sol = readSolution('maxclique/' + f)
    print(max_clique('maxclique/' + f), sol)

