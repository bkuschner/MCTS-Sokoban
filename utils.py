import numpy as np
# @param filename: filename of input
# @return: a Board made from the input file
def read_sokoban_input(filename):
    with open(filename, 'r') as f:
        # read size
        line = f.readline()
        inputs = line.split()
        size = (int(inputs[0]), int(inputs[1]))

        # read walls
        line = f.readline()
        inputs = line.split()
        inputs.pop(0)
        walls = set()
        for i in range(0, len(inputs), 2):
            walls.add((int(inputs[i]), int(inputs[i+1])))

        # read boxes
        line = f.readline()
        inputs = line.split()
        inputs.pop(0)
        boxes = set()
        for i in range(0, len(inputs), 2):
            boxes.add((int(inputs[i]), int(inputs[i + 1])))

        # read storages
        line = f.readline()
        inputs = line.split()
        inputs.pop(0)
        storages = set()
        for i in range(0, len(inputs), 2):
            storages.add((int(inputs[i]), int(inputs[i + 1])))

        # read start position
        line = f.readline()
        inputs = line.split()
        start = (int(inputs[0]), int(inputs[1]))

    return size, walls, boxes, storages, start

# @param filename: name of file containing sokoban input
# @return (rows, cols): 2-tuple containing rows and columns of sokoban board
# @return len(boxes): number of boxes in the board
# @return map: 2d list containing the board with
#  '#' for walls, '$' for boxes, '.' for storages, '@' for player, and ' ' for empty spaces
# parse sokoban input and return the dimensions of board, number of boxes, and map
def parse(filename):
    size, walls, boxes, targets, start = read_sokoban_input(filename=filename)
    cols, rows = size
    map = [[""]*cols for i in range(rows)]
    for row in range(1, rows+1):
        for col in range(1, cols+1):
            if (row, col) in walls:
                map[row-1][col-1] = "#"
            elif (row, col) in boxes:
                map[row-1][col-1] = "$"
            elif (row, col) in targets:
                map[row-1][col-1] = "."
            elif (row, col) == start:
                map[row-1][col-1] = "@"
            else:
                map[row-1][col-1] = " "
    return (rows, cols), len(boxes), map
