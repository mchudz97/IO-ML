import math


class Node:

    def __init__(self, pos: []):
        self.position = pos
        self.neighbors = []
        self.visited = False

    def is_neighbor_of(self, node):
        if math.sqrt((self.position[0] - node.position[0]) ** 2
                     + ((self.position[1]) - node.position[1]) ** 2) == 1:
            return True

        return False


class BFS:

    def __init__(self, maze: []):

        self.maze = maze.copy()
        self.start_node = None
        self.end_node = None
        self.nodes = []
        self.queue = []
        self.create_nodes()
        self.set_neighbors()
        self.queue.append(self.start_node)

    def create_nodes(self):

        for line in range(len(self.maze)):
            for char in range(len(self.maze[line])):
                if self.maze[line][char] == 'S':
                    self.start_node = Node([char, line])
                    self.nodes.append(self.start_node)
                elif self.maze[line][char] == 'E':
                    self.end_node = Node([char, line])
                    self.nodes.append(self.end_node)
                elif self.maze[line][char] == ' ':
                    self.nodes.append(Node([char, line]))

    def set_neighbors(self):

        for x in self.nodes:
            for y in self.nodes:
                if y.is_neighbor_of(x): x.neighbors.append(y)

    def print_path(self):

        path_array: [] = self.maze.copy()
        path_array = [list(sting) for sting in path_array]
        for i in self.nodes:
            if i.visited:
                path_array[i.position[1]][i.position[0]] = 'o'

        for x in path_array:
            print(*x)

        print()

    def run(self):

        while len(self.queue) != 0:
            if self.end_node in self.queue:
                self.end_node.visited = True
                break

            else:
                popped = self.queue.pop()
                popped.visited = True
                for p in popped.neighbors:
                    if not p.visited:
                        self.queue.append(p)

        self.print_path()
