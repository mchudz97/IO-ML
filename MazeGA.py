from pyeasyga import pyeasyga
import numpy as np
import matplotlib.pyplot as plt
import math
from MazeReader import MazeReader
import random

PENALTY = -.5


class MazeGA:

    def __init__(self, maze_array: [], steps: int ):

        if not maze_array or len(maze_array) == 0 or len(maze_array) != len(maze_array[0]):
            raise Exception("Invalid input value!")

        self.maze: [] = maze_array
        self.size = len(self.maze)
        self.end_position = self.find_end()
        self.start_position = self.find_start()
        self.max_steps = steps
        self.data = []

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

    def generate_chromosomes(self, amount, size):
        for i in range(amount):
            chromosome = []
            for j in range(size*2):
                chromosome[j] = random.randint(0, 1)
        self.data.append(chromosome)

    def move(self, first_num, sec_num):

        if first_num == 0 and sec_num == 0:
            if self.maze[self.current_position[1]][self.current_position[0] - 1] == '#':
                return PENALTY
            self.current_position[0] -= 1

        elif first_num == 0 and sec_num == 1:
            if self.maze[self.current_position[1]][self.current_position[0] + 1] == '#':
                return PENALTY
            self.current_position[0] += 1

        elif first_num == 1 and sec_num == 0:
            if self.maze[self.current_position[1] + 1][self.current_position[0]] == '#':
                return PENALTY
            self.current_position[1] += 1

        else:
            if self.maze[self.current_position[1] - 1][self.current_position[0]] == '#':
                return PENALTY
            self.current_position[1] -= 1

        return 0

def my_crossover(parent_1, parent_2):

    index = 0
    rand_cross_at_start = random.randrange(1, 10)
    if rand_cross_at_start < 7:
        index = random.randrange(1, int(len(parent_1)/2))
    else:
        index = random.randrange(int(len(parent_1)/2), len(parent_1))
    child_1 = parent_1[:index] + parent_2[index:]
    child_2 = parent_2[:index] + parent_1[index:]
    return child_1, child_2


def fitness_v1( individual, maze: MazeGA ):
    score = 0
    maze.current_position = maze.start_position.copy()
    for i in range(int(len(individual)/2) - 1):
        score += maze.move(individual[2*i], individual[2*i+1])
        if maze.get_distance_to_end(maze.current_position[0], maze.current_position[1]) == 0:
            score -= i * 0.1
            break
    score -= maze.get_distance_to_end(maze.current_position[0], maze.current_position[1])

    return score


def fitness_v2( individual, maze: MazeGA ):
    score = 0
    maze.current_position = maze.start_position
    for i in range(int(len(individual)/2) - 1):
        score += maze.move(individual[2*i], individual[2*i+1])
        print(maze.current_position)
        if maze.get_distance_to_end(maze.current_position[0], maze.current_position[1]) == 0:
            break
    score -= maze.get_distance_to_end(maze.current_position[0], maze.current_position[1])

    return score

def generate_charts(ga : pyeasyga.GeneticAlgorithm):
    all_vals = []
    best_vals = []
    ga.create_first_generation()
    all_vals.append([x.fitness for x in ga.current_generation])
    best_vals.append(ga.current_generation[0].fitness)
    print(ga.current_generation[0].fitness)
    for _ in range(1, ga.generations):
        ga.create_next_generation()
        all_vals.append([x.fitness for x in ga.current_generation])
        best_vals.append(ga.current_generation[0].fitness)




    avg = [np.average(x) for x in all_vals]
    fig, ax = plt.subplots()
    ax.plot(best_vals, label="Max")
    ax.plot(avg, label="Avg")
    plt.xlabel("Generations")
    plt.ylabel("Value")
    legend = ax.legend(loc='lower right')
    plt.show()




r = MazeReader('m1.txt')
mga = MazeGA(r.board, r.steps)
pga = pyeasyga.GeneticAlgorithm(mga, population_size=800, elitism=True, mutation_probability=.99, generations=100)
pga.fitness_function = fitness_v1
pga.crossover_function = my_crossover

generate_charts(pga)
