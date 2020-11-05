import math
from operator import attrgetter


class ANode:

    def __init__(self, position: []):
        self.position = position
        self.g = 0
        self.f = 0
        self.h = 0
        self.visited = False
        self.parent = None
        self.neighbors = []

    def is_neighbor_of(self, node):

        if math.sqrt((self.position[0]-node.position[0])**2
                     + ((self.position[1])-node.position[1])**2) == 1:
            return True

        return False

    def count_functions(self, end_node):

        #self.g = math.sqrt((start_node.position[0] - self.position[0]) ** 2
        #                   + (start_node.position[1] - self.position[1]) ** 2)
        #self.h = math.sqrt((end_node.position[0] - self.position[0]) ** 2
        #                   + (end_node.position[1] - self.position[1]) ** 2)

        self.g = self.parent.g +1
        self.h = abs(end_node.position[0] - self.position[0]) + abs(end_node.position[1] - self.position[1])

        self.f = self.g + self.h


class AStar:

    def __init__(self, maze: []):

        self.maze = maze.copy()
        self.nodes = []
        self.start_node = None
        self.end_node = None
        self.create_nodes()
        self.set_neighbors()
        self.queue = []
        self.queue.append(self.start_node)

    def create_nodes(self):

        for line in range(len(self.maze)):
            for char in range(len(self.maze[line])):
                if self.maze[line][char] == 'S':
                    self.start_node = ANode([char, line])
                    self.nodes.append(self.start_node)
                elif self.maze[line][char] == 'E':
                    self.end_node = ANode([char, line])
                    self.nodes.append(self.end_node)
                elif self.maze[line][char] == ' ':
                    self.nodes.append(ANode([char, line]))

    def set_neighbors(self):

        for x in self.nodes:
            for y in self.nodes:
                if y.is_neighbor_of(x): x.neighbors.append(y)

    def run(self):

        while len(self.queue) > 0 and self.end_node.visited is not True:
            best_choice = min(self.queue, key=attrgetter('f'))
            best_choice.visited = True
            self.queue.remove(best_choice)
            for n in best_choice.neighbors:
                if not n.visited:
                    self.queue.append(n)
                    n.parent = best_choice
                    n.count_functions(self.end_node)

        self.print_path()

    def print_path(self):

        path_array: [] = self.maze.copy()
        path_array = [list(sting) for sting in path_array]
        for i in self.nodes:
            if i.visited:
                path_array[i.position[1]][i.position[0]] = 'o'

        for x in path_array:
            print(*x)

        print()
