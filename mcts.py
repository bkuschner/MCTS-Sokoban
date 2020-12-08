from Board import Board
from Node import Node
import random

MAX_MOVES = 100
MAX_ROLLOUTS = 100000

# @param env: a Board that the function will attempt to solve
# @return: a list of actions to solve the board
def mcts_solve(env):
    moves = 0
    actions = []
    while not env.isTerminal() and moves <= MAX_MOVES:
        action = mcts(env)
        actions.append(action)
        env.step(action)
        moves = moves + 1
    return actions

def mcts(env):
    my_tree = Node(env)
    rollouts = 0
    while rollouts <= MAX_ROLLOUTS:
        child = select_and_expand(my_tree)
        result = simulate(child)
        back_propagate(result, child)
        rollouts = rollouts + 1

    max_rollouts = -1
    for child in my_tree.children:
        if child.rollouts > max_rollouts:
            max_rollouts = child.rollouts
            max_roll_node = child
    return max_roll_node.action

def select_and_expand(tree):
    while not tree.data.is_terminal():
        if len(tree.children) < 4:
             return expand(tree)
        else:
            tree = ucb_select(tree)

    return tree

def expand(node):
    actions = {'U', 'D', 'L', 'R'}
    for child in node.children:
        actions.remove(child.action)
    action = random.choice(tuple(actions))
    new_child = Node(node.data.step(action), node, action)
    node.children.add(new_child)
    return new_child


