from cs170proj import *

import os
import sys
import time

GRAPH_DIR = "./bestgraphs"

def get_graph_file(index):
	return GRAPH_DIR + "/graph" + str(index) + ".txt"

def replace_min(arr, new_pt):
	min_val = float('infinity')
	min_index = -1
	for i,item in enumerate(arr):
		if item[1] < new_pt[1] and item[1] < min_val:
			min_val = item[1]
			min_index = i

	if min_index > -1:
		arr[min_index] = new_pt
		writeFile(get_graph_file(min_index), new_pt[0])
	return arr

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def evaluate(str):
	return (swap_2opt_solve_str(str)[1] - greedy_solve_str(str)[1])**2

def load_graphs():
	i = 0
	arr = []
	while os.path.isfile(get_graph_file(i)):
		st = readFile(get_graph_file(i))
		score = evaluate(st)
		arr.append([st, score])
		i += 1
	return arr

def generate_graphs(number):
	arr = []
	for i in range(number):
		st = generate_graph(50, 0, 100)
		writeFile(get_graph_file(i), st)
		score = evaluate(st)
		arr.append([st, score])
	return arr

def initLearner(n, stop):
	ensure_dir(GRAPH_DIR)

	#hay algun?
	if os.path.isfile(get_graph_file(0)):
		arr = load_graphs()
	else:
		arr = generate_graphs(n)

	run(arr, stop)

def run(arr, stop):
	while time.time() < stop:
		st = generate_graph(50, 0, 100)
		score = evaluate(st)
		arr = replace_min(arr, [st, score])

if __name__ == '__main__':
	stop = time.time() + float(sys.argv[2])
	n = int(sys.argv[1])
	initLearner(n, stop)


