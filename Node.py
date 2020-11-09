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


class ANode(Node):

    def __init__(self, position: []):
        super().__init__(position)

        self.g = 0
        self.f = 0
        self.h = 0
        self.parent = None

    def count_functions(self, end_node):

        self.g = self.parent.g + 1
        self.h = abs(end_node.position[0] - self.position[0]) + abs(end_node.position[1] - self.position[1])
        self.f = self.g + self.h
