from anytree import NodeMixin
class Node(NodeMixin):
    def __init__(self, name, state, last_pos = None, move_box = True, done = False, action = None, parent = None, children = None):
        super(Node, self).__init__()
        self.name = name
        self.state = state
        self.done = done
        self.utility = 0
        self.rollouts = 0
        self.last_pos = last_pos
        self.move_box = move_box
        self.parent = parent
        self.action = action
        if children:
            self.children = children