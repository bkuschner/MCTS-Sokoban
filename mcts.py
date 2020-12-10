import gym_sokoban
from Node import Node
import random
import numpy as np
from math import sqrt, log

ACTION_LOOKUP = {
    0: 'no operation',
    1: 'push up',
    2: 'push down',
    3: 'push left',
    4: 'push right',
    5: 'move up',
    6: 'move down',
    7: 'move left',
    8: 'move right',
}

class MCTS:
    def __init__(self, env, max_rollouts = 10000, max_depth = 30, actions = [1,2,3,4]):
        self.env = env
        self.max_rollouts = max_rollouts
        self.max_depth = max_depth
        self.actions = actions
        # env_state := boxes_on_target(int), num_env_steps(int), player_position(numpy array), room_state(numpy array)
        
# @param env: a Board that the function will attempt to solve
# @return: a list of actions to solve the board
    def take_best_action(self, observation_mode="rgb_array"):
        env_state = self.env.get_current_state()
        best_action = self.mcts(env_state)
        observation, reward, done, info = self.env.step(best_action, observation_mode=observation_mode)
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
        for child in root.children:
            print(ACTION_LOOKUP[child.action], child.utility, child.rollouts)
        best_child = max(root.children, key= lambda child: child.rollouts)
        return best_child.action

    def select_and_expand(self, tree):
        while not tree.done:
            if len([child.action for child in tree.children]) < len(self.actions):
                return self.expand(tree)
            else:
                tree = self.ucb_select(tree)

        return tree

    def expand(self, node):
        untried_actions = set(self.actions) - set([child.action for child in node.children])
        action = random.choice(tuple(untried_actions))
        state, observation, reward_last, done, info = self.env.simulate_step(action=action, state=node.state) # I don't know if this immediate reward is important to the child node
        new_child = Node(state, done=done, parent=node, action=action)
        new_child.utility = reward_last
        node.children.append(new_child)
        return new_child

    def ucb_select(self, tree):
        max_value = -1
        for child in tree.children:
            # avoid divide by 0
            if child.rollouts == 0:
                #FATAL ERROR
                exit(-1)
                return child
            child_value = (child.utility / child.rollouts) + (sqrt(2) * log(tree.rollouts) / child.rollouts)
            if child_value > max_value:
                max_value = child_value
                max_node = child
        return max_node

    def simulate(self, node):
        depth = 0
        total_reward = 0
        state = node.state
        done = node.done
        while not done and depth < self.max_depth:
            action = random.choice(self.actions)
            state, observation, reward, done, info = self.env.simulate_step(action=action, state=state)
            total_reward = total_reward + reward
            depth = depth + 1
        return total_reward + self.heuristic(node)

    def heuristic(self, node):
        total = 0
        arr_goals = (self.env.room_fixed == 2)
        arr_boxes = ((node.state[3] == 4) + (node.state[3] == 3))
        # find distance between each box and its nearest storage
        for i in range(len(arr_boxes)):
            for j in range(len(arr_boxes[i])):
                if arr_boxes[i][j] == 1: # found a box
                    min_dist = 9999999
                    # check every storage
                    for k in range(len(arr_goals)):
                        for l in range(len(arr_goals[k])):
                            if arr_goals[k][l] == 1: # found a storage
                                min_dist = min(min_dist, abs(i - k) + abs(j - l))
                    total = total + min_dist
        return total * self.env.penalty_for_step

    # TODO: check if this actually works #IT WORKS
    def back_propagate(self, result, node):
        while node is not None:
            node.utility = node.utility + result
            result += self.env.penalty_for_step
            node.rollouts = node.rollouts + 1
            node = node.parent
