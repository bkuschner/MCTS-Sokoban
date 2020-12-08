class Node:
    def __init__(self, state, done = False, parent = None, action = None):
        self.state = state
        self.done = done
        self.children = []
        self.utility = 0
        self.rollouts = 0
        self.parent = parent
        self.action = action