from random import randint, random, shuffle
from itertools import permutations, groupby

import time

#from UnionFind import UnionFind
#from Graphs import isUndirected

import sys

def swap_3opt(path, i, j, k):
    return [path[:i] + t[0] + t[1] + t[2] for t in list(permutations([path[i:j], path[j:k], path[k:]]))]# + list(permutations([path[:i], path[j:i-1:-1], path[j-1:k], path[k+1:]])) + list(permutations([path[:i], path[j:i-1:-1], path[k:j-1:-1], path[k+1:]])) + list(permutations([path[:i], path[i-1:j], path[k:j-1:-1], path[k+1:]]))

def swap_3opt_optimize_path(path, arr, colors, size):
    best_distance = get_cost_graph(arr, path)
    for i in range(1, size - 2):
        for j in range(i+1, size - 1):
            for k in range(j+1, size):
                #print str(i) + " " + str(j) + " " + str(k)
                new_routes = swap_3opt(path, i, j, k)
                for l in range(6):
                    #new_routes[l] = new_routes[l][0] + new_routes[l][1] + new_routes[l][2] + new_routes[l][3]
                    if is_valid_path(colors, new_routes[l]):
                        if get_cost_graph(arr, new_routes[l]) < best_distance:
                            return new_routes[l]
                            """best_path = new_routes[l]
                            best_distance = get_cost_graph(arr, new_routes[l])
                new_routes = [sum(route, []) for route in new_routes if is_valid_path(colors, sum(route, []))]
                if len(new_routes):
                    new_route = min(new_routes,key=lambda x: get_cost_graph(arr, x))

                    if(get_cost_graph(arr, new_route) < best_distance):
                        return new_route"""
    #print "finished 1 3opt"
    return path

def swap_kopt_solve_path(arr, colors, size, path):
    best_distance = get_cost_graph(arr, path)
    while True:
        new_path = swap_2opt_optimize_path(path, arr, colors, size)
        if new_path != path:
            path = new_path
        else:
            new_path = swap_3opt_optimize_path(path, arr, colors, size)
            if new_path != path:
                path = new_path
            else:
                break
    if not is_valid_path(colors, path):
        print "NOT VALID"
    return [path, get_cost_graph(arr, path)]

def swap_kopt_solve_str(str):
    dic = parse_graph(str)
    path,best_distance = greedy_solve_str(str)
    return swap_kopt_solve_path(dic['arr'], dic['colors'], dic['size'], path)


def swap_2opt(path, i, j):
    return path[:i] + path[j:i-1:-1] + path[j+1:]

def swap_2opt_optimize_path(path, arr, colors, size):
    best_distance = get_cost_graph(arr, path)
    for i in range(1,size - 1):
        for j in range(i+1,size):
            new_route = swap_2opt(path, i,j)
            if is_valid_path(colors, new_route):
                if best_distance > get_cost_graph(arr, new_route):
                    return new_route
    return path

def swap_2opt_solve_path(arr, colors, size, path):
    best_distance = get_cost_graph(arr, path)
    while True:
        new_path = swap_2opt_optimize_path(path, arr, colors, size)
        if new_path != path:
            path = new_path
        else:
            break
    return [path, get_cost_graph(arr, path)]


def swap_2opt_solve_str(str):
    dic = parse_graph(str)
    path,best_distance = greedy_solve_str(str)
    return swap_2opt_solve_path(dic['arr'], dic['colors'], dic['size'], path)


# sauce: https://www.ics.uci.edu/~eppstein/PADS/MinimumSpanningTree.py
"""
def MinimumSpanningTree(G):
"""
"""
Return the minimum spanning tree of an undirected graph G.
G should be represented in such a way that iter(G) lists its
vertices, iter(G[u]) lists the neighbors of u, G[u][v] gives the
length of edge u,v, and G[u][v] should always equal G[v][u].
The tree is returned as a list of edges.
"""
"""
if not isUndirected(G):
    raise ValueError("MinimumSpanningTree: input is not undirected")
for u in G:
    for v in G[u]:
        if G[u][v] != G[v][u]:
            raise ValueError("MinimumSpanningTree: asymmetric weights")

# Kruskal's algorithm: sort edges by weight, and add them one at a time.
# We use Kruskal's algorithm, first because it is very simple to
# implement once UnionFind exists, and second, because the only slow
# part (the sort) is sped up by being built in to Python.
subtrees = UnionFind()
tree = []
for W,u,v in sorted((G[u][v],u,v) for u in G for v in G[u]):
    if subtrees[u] != subtrees[v]:
        tree.append((u,v))
        subtrees.union(u,v)
return tree    
"""

def get_cost_graph(arr, path):
    su = 0
    for i in range(len(path) - 1):
        su += arr[path[i]][path[i+1]]
    return su

def is_valid_path(colors, path):
    color = [colors[p] for p in path]
    return len([k for k,g in groupby(color) if sum(1 for i in g) > 3]) == 0

def greedy_solve_from_point(index, arr, colors, size):
    path = [index]
    visited = [index]
    color = colors[index]
    color_count = 1
    cur_node = index
    while len(path) < size:
        if color_count < 3:
            choices = [[i, d] for i,d in enumerate(arr[cur_node]) if i not in path]
        else:
            choices = [[i, d] for i,d in enumerate(arr[cur_node]) if i not in path and colors[i] != color]
        if len(choices) == 0:
            #print path
            temp = range(size)
            while not is_valid_path(colors, temp):
                shuffle(temp)
            return [temp, get_cost_graph(arr, temp)]
            #choices = [[i, d] for i,d in enumerate(arr[cur_node]) if i not in path]
            #return [[], float("infinity")]
            #a = path.pop()
            #forbidden.append(a)
            #continue
        forbidden = []
        new_node = min(choices,key=lambda x: x[1])
        path.append(new_node[0])
        if colors[new_node[0]] == color:
            color_count += 1
        else:
            color_count = 1
            color = colors[new_node[0]]
        cur_node = new_node[0]
    return [path, get_cost_graph(arr, path)]

def greedy_solve_str(str):
    dic = parse_graph(str)
    return min([greedy_solve_from_point(i, dic['arr'], dic['colors'], dic['size']) for i in range(dic['size'])],key=lambda x: x[1])

def greedy_solve_all_str(str):
    dic = parse_graph(str)
    solns = [greedy_solve_from_point(i, dic['arr'], dic['colors'], dic['size']) for i in range(dic['size'])]
    min_value = min(solns,key=lambda x: x[1])[1]
    return filter(lambda (x,y): y == min_value, solns)

def brute_force_solve_str(str):
    dic = parse_graph(str)
    return min([[item, get_cost_graph(dic['arr'], item)] for item in list(permutations(range(dic['size']))) if is_valid_path(dic['colors'], item)], key=lambda x: x[1])

def brute_force_solve_str_all(str):
    dic = parse_graph(str)
    solns = [[item, get_cost_graph(dic['arr'], item)] for item in list(permutations(range(dic['size']))) if is_valid_path(dic['colors'], item)]
    min_value = min(solns,key=lambda x: x[1])[1]
    return filter(lambda (x,y): y == min_value, solns)

def parse_graph(str):
    lines = str.strip().replace("\r", "").split("\n")
    n = int(lines[0])
    colors = lines.pop()
    arr = [[int(a) for a in li.replace("\t", " ").strip().split()] for li in lines[1:]]
    return {'size' : n, 'colors' : colors, 'arr' : arr}

def check_valid(str):
    lines = str.split("\n")
    line = lines[0].split()
    if len(line) != 1 or not line[0].isdigit():
        return False,"Line 1 must contain a single integer."
    N = int(line[0])
    if N < 4 or N > 50 or N % 2 != 0:
        return False,"N must be an even integer between 4 and 50, inclusive."
    d = [[0 for j in range(N)] for i in range(N)]
    for i in xrange(N):
        line = lines[i + 1].split()
        if len(line) != N:
            return False,"Line " + `i+2` + " must contain N integers."
        for j in xrange(N):
            if not line[j].isdigit():
                return False,"Line " + `i+2` + " must contain N integers."
            d[i][j] = int(line[j])
            a = int(line[j])
            if d[i][j] < 0 or d[i][j] > 100:
                return False,"All edge weights must be between 0 and 100, inclusive."
    for i in xrange(N):
        if d[i][i] != 0:
            return False,"The distance from a node to itself must be 0."
        for j in xrange(N):
            if d[i][j] != d[j][i]:
                return False,"The distance matrix must be symmetric."
    line = lines[len(lines) - 1]
    if len(line) != N:
        return False,"Line " + `N+2` + " must be a string of length N."
    r = 0
    b = 0
    for j in xrange(N):
        c = line[j]
        if c != 'R' and c != 'B':
            return False,"Each character of the string must be either R or B."
        if c == 'R': r += 1
        if c == 'B': b += 1
    if r != b:
        return False,"The number of red and blue cities must be equal."
    return True,"ok"

def generate_graph(size, minDist, maxDist):
    arr = [[str(randint(minDist, maxDist)) for i in range(size)] for item in range(size)]
    for i in range(size):
        arr[i][i] = "0"
        for j in range(size):
            arr[j][i] = arr[i][j]
    colors = "R"*(size/2) + "B"*(size/2)
    colors = list(colors)
    shuffle(colors)
    solution = str(size) + "\n" + "\n".join([' '.join(row) for row in arr]) + "\n" + ''.join(colors)
    validity = check_valid(solution)
    if validity[0]:
        return solution
    return generate_graph(size, minDist, maxDist)

def generate_graph_with_path(size, minDist, maxDist):
    # Abandoned with bug
    count = 100
    arr = [[str(count) for i in range(size)] for item in range(size)]
    for i in range(size):
        rand = randint(0, size-1)
        arr[i][rand] = str(randint(minDist, maxDist/2))
        arr[i][i] = "0"
        for j in range(size):
            arr[j][i] = arr[i][j]
    colors = "R"*(size/2) + "B"*(size/2)
    colors = list(colors)
    shuffle(colors)
    solution = str(size) + "\n" + "\n".join([' '.join(row) for row in arr]) + "\n" + ''.join(colors)
    validity = check_valid(solution)
    if validity[0]:
        while (greedy_solve_str(solution)[1] - swap_2opt_solve_str(solution)[1] == 0) and (count > maxDist/2):
            arr = parse_graph(solution)['arr']
            for i in range(size):
                for j in range(size):
                    if arr[j][i] == count:
                        arr[j][i] -= 1
                        arr[i][j] -= 1
                    arr[j][i] = str(arr[j][i])
                    arr[i][j] = str(arr[i][j])
            count -= 1
            solution = str(size) + "\n" + "\n".join([' '.join(row) for row in arr]) + "\n" + ''.join(colors)
            print(solution)
        return solution
    return generate_graph_with_path(size, minDist, maxDist)

def writeFile(file, str):
    f = open(file, "w")
    f.write(str)
    f.close()

def readFile(file):
    f = open(file, "r")
    return f.read().replace("\r", "")

def solveFromFile(file, doBruteForce):
    f = open(file, "r")
    st = f.read().strip()
    if doBruteForce:
        print brute_force_solve_str_all(st)
    # print greedy_solve_str(st)
    # print greedy_solve_all_str(st)
    print swap_2opt_solve_str(st)

def solveFromFileForLength(file):
    f = open(file, "r")
    st = f.read().strip()
    return greedy_solve_str(st)[1] - swap_2opt_solve_str(st)[1]

def solveFromFileBest(file):
    f = open(file, "r")
    st = f.read().strip()
    greed = greedy_solve_str(st)
    two_opt = swap_2opt_solve_str(st)
    if greed[1] < two_opt[1]:
        return greed[0]
    else:
        return two_opt[0]

def getBestGraphs():
    lst = []
    i = 0
    while i < 100:
        print(i)
        lst.append((solveFromFileForLength("./bestgraphs/graph"+str(i)+".txt"), i))
        i += 1
    lst = sorted(lst, reverse=True)
    print lst

def solveFromFiles(i, j):
    for k in range(i, j):
        a = time.clock()
        st = readFile("./instances/"+str(k)+".in")
        sol = swap_kopt_solve_str(st)
        writeFile("./solutions/"+str(k)+".out", str(sol))
        print "Solved " + str(k) + " in " + str(time.clock()-a) + "s"

def readAllSolutions(mx):
    sol = ""
    for i in range(1, mx):
        st = readFile("./solutions/"+str(i)+".out")
        arr = eval(st)[0]
        if 0 in arr:
            arr = [j + 1 for j in arr]
        sol += ' '.join([str(j) for j in arr]) + "\n"
    writeFile("./masterOutput.out", sol)

def readAllFiles():
    final_str = ""
    i = 1
    while i < 496:
        if i !=  2 and i != 10:
            print(i)
            final_str += str(solveFromFileBest("./instances/"+str(i)+".in")) +"\n"
        i += 1
    writeFile("./answer.out", final_str)

if __name__ == '__main__':
    readAllSolutions(496)
    #solveFromFiles(41, 42)

    #solveFromFiles(300, 450)
#     graph = generate_graph(8,0,50)
#     print brute_force_solve_str(graph)
#     print greedy_solve_str(graph)
#     print swap_2opt_solve_str(graph)
#     print greedy_solve_all_str(graph)
#     print swap_kopt_solve_str(graph)

#     graph = generate_graph(50,0,100)
#     print greedy_solve_str(graph)
#     print swap_2opt_solve_str(graph)
#     print greedy_solve_all_str(graph)
#     a = time.clock()
#     print swap_kopt_solve_str(graph)
#     print str(time.clock() - a)
