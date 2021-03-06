from time import time_ns

from pyeasyga import pyeasyga
import numpy as np
import matplotlib.pyplot as plt
import math

from AStar import AStar
from BFS import BFS
from MazeReader import MazeReader
import random

PENALTY = 1


class MazeGA:

    def __init__(self, maze_array: [], steps: int ):

        if not maze_array or len(maze_array) == 0 or len(maze_array) != len(maze_array[0]):
            raise Exception("Invalid input value!")

        self.maze: [] = maze_array
        self.size = len(self.maze)
        self.end_position = self.find_end()
        self.start_position = self.find_start()
        self.max_steps = steps

    def __len__(self):

        return self.max_steps * 2

    def get_distance_to_end(self, pos_x, pos_y):

        return math.sqrt((self.end_position[0]-pos_x)**2 + ((self.end_position[1])-pos_y)**2)

    def find_end(self):

        for line in self.maze:
            x = line.find('E')
            if x != -1:

                return [x, self.maze.index(line)]

        raise Exception("End char not found!")

    def find_start(self):

        for line in self.maze:
            x = line.find('S')
            if x != -1:
                return [x, self.maze.index(line)]

        raise Exception("Start char not found!")

    def move(self, first_num, sec_num, pos: []):

        if first_num == 0 and sec_num == 0:
            if self.maze[pos[1]][pos[0] - 1] == '#':
                return PENALTY
            pos[0] -= 1

        elif first_num == 0 and sec_num == 1:
            if self.maze[pos[1]][pos[0] + 1] == '#':
                return PENALTY
            pos[0] += 1

        elif first_num == 1 and sec_num == 0:
            if self.maze[pos[1] + 1][pos[0]] == '#':
                return PENALTY
            pos[1] += 1

        else:
            if self.maze[pos[1] - 1][pos[0]] == '#':
                return PENALTY
            pos[1] -= 1

        return 0


def my_crossover(parent_1, parent_2):

    rand_cross_at_start = random.randrange(1, 10)
    if rand_cross_at_start < 7:
        index = random.randrange(1, int(len(parent_1)/2))
    else:
        index = random.randrange(int(len(parent_1)/2), len(parent_1))
    child_1 = parent_1[:index] + parent_2[index:]
    child_2 = parent_2[:index] + parent_1[index:]
    return child_1, child_2


def fitness_v1(individual, maze: MazeGA):

    score = 0
    maze.current_position = maze.start_position.copy()
    for i in range(int(len(individual)/2) - 1):
        maze.move(individual[2*i], individual[2*i+1], maze.current_position)
        if maze.get_distance_to_end(maze.current_position[0], maze.current_position[1]) == 0:
            return 0
    score -= maze.get_distance_to_end(maze.current_position[0], maze.current_position[1])

    return score


def fitness_v2(individual, maze: MazeGA):

    score = 0
    prev_pos = []
    maze.current_position = maze.start_position.copy()
    prev_pos.append(maze.current_position.copy())

    for i in range(int(len(individual)/2) - 1):
        inc_pos = maze.current_position.copy()
        maze.move(individual[2*i], individual[2*i+1], inc_pos)
        is_in = False
        for pos in prev_pos:
            if pos == inc_pos:
                score -= PENALTY
                is_in = True
                break
        if is_in:
            continue
        prev_pos.append(inc_pos.copy())
        maze.current_position = inc_pos

        if maze.get_distance_to_end(maze.current_position[0], maze.current_position[1]) == 0:
            return 0

    score -= maze.get_distance_to_end(maze.current_position[0], maze.current_position[1])

    return score


def print_path(mga_obj: MazeGA, chromosome: pyeasyga.Chromosome, fitness_type):

    pos = mga_obj.start_position.copy()
    path_array: [] = mga_obj.maze.copy()
    path_array = [list(sting) for sting in path_array]
    print()
    if fitness_type == fitness_v1:

        for i in range(int(len(chromosome.genes) / 2) - 1):
            mga_obj.move(chromosome.genes[2*i], chromosome.genes[2*i+1], pos)
            path_array[pos[1]][pos[0]] = 'o'
            if mga_obj.get_distance_to_end(pos[0], pos[1]) == 0:
                break

    elif fitness_type == fitness_v2:

        prev_pos = [pos.copy()]
        for i in range(int(len(chromosome.genes) / 2) - 1):
            inc_pos = pos.copy()
            mga_obj.move(chromosome.genes[2*i], chromosome.genes[2*i+1], inc_pos)

            is_in = False
            for p in prev_pos:
                if p == inc_pos:
                    is_in = True
                    break
            if is_in:
                continue
            prev_pos.append(inc_pos.copy())

            pos = inc_pos
            path_array[pos[1]][pos[0]] = 'o'
            if mga_obj.get_distance_to_end(pos[0], pos[1]) == 0:
                break


    for x in path_array:
        print(*x)

    print()

def generate_charts(ga : pyeasyga.GeneticAlgorithm):

    all_vals = []
    best_vals = []
    start = time_ns()
    ga.create_first_generation()
    all_vals.append([x.fitness for x in ga.current_generation])
    best_vals.append(ga.current_generation[0].fitness)

    for _ in range(1, ga.generations):

        if ga.current_generation[0].fitness == 0:
            break
        ga.create_next_generation()
        all_vals.append([x.fitness for x in ga.current_generation])
        best_vals.append(ga.current_generation[0].fitness)

    print(f'\nin {(time_ns() - start) / 1000000}ms')
    avg = [np.average(x) for x in all_vals]
    fig, ax = plt.subplots()
    ax.plot(best_vals, label="Max")
    ax.plot(avg, label="Avg")
    plt.xlabel("Generations")
    plt.ylabel("Value")
    legend = ax.legend(loc='lower right')
    plt.show()

r = MazeReader('m4.txt')
mga = MazeGA(r.board, r.steps)
pga = pyeasyga.GeneticAlgorithm(mga, population_size=5000,
                                elitism=True,
                                mutation_probability=.1,
                                generations=50)
pga.fitness_function = fitness_v2
pga.crossover_function = my_crossover

bfs = BFS(mga.maze)
bfs.run()

ast = AStar(mga.maze)
ast.run()

generate_charts(pga)
print_path(mga, pga.current_generation[0], pga.fitness_function)


