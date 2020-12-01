from Board import Board


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

    return Board(size, walls, boxes, storages, start)
