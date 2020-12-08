class Node:
    def __init__(self, data, parent = None, action = None):
        self.data = data
        self.children = {}
        self.utility = 0
        self.rollouts = 0
        self.parent = parent
        self.action = action