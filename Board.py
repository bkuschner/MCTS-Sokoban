class Board:
    # format of coordinates is (row, column) 1-indexed
    # @param size: a list with num columns and num rows
    # @param walls: a set of tuples each containing coordinates of walls
    # @param walls: a set of tuples each containing coordinates of boxes
    # @param walls: a set of tuples each containing coordinates of storage
    # @param start: a tuple containing coordinates of start space
    def __init__(self, size, walls, boxes, storages, start):
        self.columns = size[0]
        self.rows = size[1]
        self.walls = walls
        self.boxes = boxes
        for box in boxes:
            box = list(box)
        self.storages = storages
        self.player = list(start)

    def print(self):
        for row in range(1, self.rows+1):
            for column in range(1, self.columns+1):
                if (row, column) in self.walls:
                    print('#', end='')
                elif (row, column) in self.boxes:
                    print('$', end='')
                elif (row, column) in self.storages:
                    print('.', end='')
                elif [row, column] == self.player:
                    print('@', end='')
                else:
                    print(' ', end='')
            print(end='\n')

    # @return: true if all storages have a box, false otherwise
    # terminal test for a board
    def is_terminal(self):
        for storage in self.storages:
            if storage not in self.boxes:
                return False
        return True

    # @param action: char with value 'U', 'D', 'L', or 'R'
    # advance the board with one move. invalid moves do not affect the board
    def step(self, action):
        if action == 'U':
            new_player_loc = (self.player[0] - 1, self.player[1])
            new_box_loc = (self.player[0] - 2, self.player[1])
        elif action == 'D':
            new_player_loc = (self.player[0] + 1, self.player[1])
            new_box_loc = (self.player[0] + 2, self.player[1])
        elif action == 'L':
            new_player_loc = (self.player[0], self.player[1] + 1)
            new_box_loc = (self.player[0], self.player[1] + 2)
        elif action == 'R':
            new_player_loc = (self.player[0], self.player[1] + 1)
            new_box_loc = (self.player[0], self.player[1] + 2)
        else:
            return self

        # action would put player out of bounds
        if new_player_loc[0] < 1 or new_player_loc[0] > self.rows or new_player_loc[1] < 1\
                or new_player_loc[1] > self.columns:
            return self
        # action would move the player into a wall
        elif new_player_loc in self.walls:
            return self
        elif new_player_loc in self.boxes:
            # action would move the box out of bounds
            if new_box_loc[0] < 1 or new_box_loc[0] > self.rows or new_box_loc[1] < 1 or new_box_loc[1] > self.columns:
                return self
            # action would move the box into a wall
            elif new_box_loc in self.walls:
                return self
            self.boxes.remove(new_player_loc)
            self.boxes.add(new_box_loc)

        self.player = new_player_loc
        return self
