import numpy as np

class SokobanEnv:
    # format of coordinates is (row, column) 1-indexed
    # @param size: a list with num columns and num rows
    # @param walls: a set of tuples each containing coordinates of walls
    # @param walls: a set of tuples each containing coordinates of boxes
    # @param walls: a set of tuples each containing coordinates of storage
    # @param start: a tuple containing coordinates of start space
    def __init__(self, size, walls, boxes, storage, start):
        self.columns, self.rows = size
        self.walls = walls
        self.boxes = boxes
        self.storage = storage
        self.start = start

    def print(self):
        for row in range(1, self.rows+1):
            for column in range(1, self.columns+1):
                if (row, column) in self.walls:
                    print('#', end='')
                elif (row, column) in self.boxes:
                    print('$', end='')
                elif (row, column) in self.storage:
                    print('.', end='')
                elif (row, column) == self.start:
                    print('@', end='')
                else:
                    print(' ', end='')
            print(end='\n')
