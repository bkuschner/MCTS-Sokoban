import gym_sokoban
from Node import Node
import random
import numpy as np
from math import sqrt, log



class MCTS:
    def __init__(self, env, max_rollouts = 10000, max_depth = 30, actions = np.array([1,2,3,4])):
        self.env = env
        self.max_rollouts = max_rollouts
        self.max_depth = max_depth
        self.actions = actions
        # env_state := boxes_on_target(int), num_env_steps(int), player_position(numpy array), room_state(numpy array)
        
# @param env: a Board that the function will attempt to solve
# @return: a list of actions to solve the board
    def take_best_action(self):
        env_state = self.env.get_current_state()
        best_action = self.mcts(env_state)
        observation, reward, done, info = self.env.step(best_action)
        return observation, reward, done, info

    # @param env: a mcts_sokoban_env that we are trying to find best move for
    # @return: best move found for the given env
    def mcts(self, env_state):
        root = Node(env_state)
        while root.rollouts <= self.max_rollouts:
            child = self.select_and_expand(root)
            result = self.simulate(child)
            self.back_propagate(result, child)
            root.rollouts += 1

        # find and return the action that got rolled out the most
        best_child = max(root.children, key= lambda child: child.rollouts)
        return best_child.action

    def select_and_expand(self, tree):
        while not tree.done:
            if len([child.action for child in tree.children]) != len(self.actions):
                return self.expand(tree)
            else:
                tree = self.ucb_select(tree)

        return tree

    def expand(self, node):
        untried_actions = set(self.actions) - set([child.action for child in node.children])
        action = random.choice(tuple(untried_actions))
        state, observation, reward_last, done, info = self.env.simulate_step(action=action, state=node.state)
        new_child = Node(state, done=done, parent=node, action=action)
        node.children.append(new_child)
        return new_child

    def ucb_select(self, tree):
        valid_children = [child for child in tree.children if child.rollouts > 0]
        best_child = max(valid_children, key = lambda child: ((child.utility / child.rollouts) + (sqrt(2) * log(tree.rollouts) / child.rollouts)))
        return best_child

    def simulate(self, node):
        pass