import queue

class Node:
    def __init__(self, state, done = False, parent = None, action = None):
        self.state = state
        self.done = done
        self.children = []
        self.utility = 0
        self.rollouts = 0
        self.parent = parent
        self.action = action

    def print_tree(self):
        print("tree:")
        frontier = queue.Queue()
        frontier.put(self)
        while not frontier.empty():
            current_node = frontier.get()
            for child in current_node.children:
                frontier.put(child)
            #print("utility: " + str(current_node.utility))
            #print("roullouts: " + str(current_node.rollouts))
            print("children: " + str(len(current_node.children)))

