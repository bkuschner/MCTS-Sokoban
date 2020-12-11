import queue
from anytree import NodeMixin
class Node(NodeMixin):
    def __init__(self, name, state, done = False, action = None, parent = None, children = None):
        super(Node, self).__init__()
        self.name = name
        self.state = state
        self.done = done
        self.utility = 0
        self.rollouts = 0
        self.parent = parent
        self.action = action
        if children:
            self.children = children
'''
    def print_tree(self):
        print("tree:")
        frontier = queue.Queue()
        frontier.put(self)
        while not frontier.empty():
            current_node = frontier.get()
            for child in current_node.children:
                frontier.put(child)
            print("utility: " + str(current_node.utility))
            print("roullouts: " + str(current_node.rollouts))
            print("children: " + str(len(current_node.children)))
'''
