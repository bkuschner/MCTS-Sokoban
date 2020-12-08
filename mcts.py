import gym_sokoban
from Node import Node
import random
from math import sqrt, log

MAX_ROLLOUTS = 100000

# @param env: a Board that the function will attempt to solve
# @return: a list of actions to solve the board
def mcts_solve(env):
    actions = []
    while not env._check_if_done():
        action = mcts(env)
        actions.append(action)
        env.step(action)
    return actions

# @param env: a mcts_sokoban_env that we are trying to find best move for
# @return: best move found for the given env
def mcts(env):
    my_tree = Node(env)
    rollouts = 0
    while rollouts <= MAX_ROLLOUTS:
        child = select_and_expand(my_tree)
        result = simulate(child)
        back_propagate(result, child)
        rollouts = rollouts + 1

    # find and return the action that got rolled out the most
    max_rollouts = -1
    for child in my_tree.children:
        if child.rollouts > max_rollouts:
            max_rollouts = child.rollouts
            max_roll_node = child
    return max_roll_node.action

def select_and_expand(tree):
    while not tree.data.is_terminal():
        if len(tree.children) < 4: # prob shouldn't hard code 4
             return expand(tree)
        else:
            tree = ucb_select(tree)

    return tree

def expand(node):
    actions = {'1', '2', '3', '4'}
    for child in node.children:
        actions.remove(child.action)
    action = random.choice(tuple(actions))
    new_child = Node(node.data.step(action), node, action)
    node.children.add(new_child)
    return new_child

def ucb_select(tree):
    max_value = -1
    for child in tree.children:
        # avoid divide by 0
        if child.rollouts == 0:
            return child
        child_value = (child.utility / child.rollouts) + (sqrt(2) * log(tree.rollouts) / child.rollouts)
        if child_value > max_value:
            max_value = child_value
            max_node = child
    return max_node

def simulate(node):
