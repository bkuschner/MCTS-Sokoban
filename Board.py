class Board:
    # @param size: a list with num columns and num rows
    # @param walls: a list of tuples each containing coordinates of walls in (x,y) format
    # @param walls: a list of tuples each containing coordinates of boxes in (x,y) format
    # @param walls: a list of tuples each containing coordinates of storage in (x,y) format
    # @param start: a tuple containing coordinates of start space in (x,y) format
    def __init__(self, size, walls, boxes, storage, start):
        self.columns = size[0]
        self.rows = size[1]
        self.walls = walls
        self.boxes = boxes
        self.storage = storage
        self.start = start
