from dimacs import *
from os import listdir
from os.path import isfile, join
from LexBFS import lex_bfs



def vertex_cover(name):
    lex_order, g = lex_bfs(name)
    n = len(lex_order)
    vertices = set()
    count = 0
    for x in lex_order[::-1]:
        empty_int = True
        for s in g[x]:
            if s in vertices:
                empty_int = False
                break
        if empty_int:
            vertices.add(x)
            count += 1
    return n - count


file_names = [f for f in listdir('vcover') if isfile(join('vcover', f))]
for f in file_names:
    sol = readSolution('vcover/' + f)
    print(vertex_cover('vcover/' + f), sol)