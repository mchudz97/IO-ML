


class MazeReader:

    def __init__(self, filename : str):

        with open(filename) as example:
            self.board = example.readlines()

        self.board = [row.rstrip('\n') for row in self.board]
        self.steps = int(self.board[-1])
        self.board.pop()

    def __str__(self):

        return '\n'.join(self.board)


