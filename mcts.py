import gym_sokoban
from Node import Node
import random
import numpy as np
from math import sqrt, log
from anytree import RenderTree

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
    def __init__(self, env, max_rollouts = 10000, max_depth = 30, actions = [1,2,3,4], verbose = False):
        self.env = env
        self.step = 0
        self.max_rollouts = max_rollouts
        self.max_depth = max_depth
        self.actions = actions
        self.penalty_for_step = env.penalty_for_step
        self.reward_finished = env.reward_finished + env.reward_box_on_target
        self.num_boxes= env.num_boxes
        self.room_fixed = env.room_fixed
        self.verbose = verbose
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
        root = Node("0",env_state)
        rollouts = 0
        while rollouts <= self.max_rollouts:
            child, immediate_reward = self.select_and_expand(root)
            result = self.simulate(child, immediate_reward)
            self.back_propagate(result, child)
            rollouts += 1

        if self.verbose:
            for pre, fill, node in RenderTree(root):
                treestr = u"%s%s" % (pre, node.name)
                print(treestr.ljust(8), node.utility/ node.rollouts, node.rollouts)
                
        best_child = max(root.children, key= lambda child: child.rollouts)
        return best_child.action

    def select_and_expand(self, tree):
        while not tree.done:
            sensible_actions = self.sensible_actions(tree.state[2], tree.state[3])
            if len([child.action for child in tree.children]) < len(sensible_actions):
                return self.expand(tree, sensible_actions)
            else:
                tree = self.ucb_select(tree)
        if self.num_boxes == tree.state[0]:
            return tree, self.reward_finished
        else:
            return tree, 0

    def expand(self, node, sensible_actions):
        untried_actions = set(sensible_actions) - set([child.action for child in node.children])
        action = random.choice(tuple(untried_actions))
        state, observation, reward_last, done, info = self.env.simulate_step(action=action, state=node.state)
        new_child = Node(name=node.name +"-{}".format(action) , state=state, done=done, parent=node, action=action)
        return new_child, reward_last

    def ucb_select(self, tree):
        best_child = max(tree.children, key = lambda child: ((child.utility / child.rollouts) + (sqrt(2) * log(tree.rollouts) / child.rollouts)))
        return best_child

    def simulate(self, node, immediate_reward):
        depth = 0
        total_reward = immediate_reward
        state = node.state
        done = node.done
        while not done and depth < self.max_depth:
            action = random.choice(self.sensible_actions(state[2], state[3]))
            state, observation, reward, done, info = self.env.simulate_step(action=action, state=state)
            total_reward = total_reward + reward
            depth = depth + 1
        return total_reward + self.heuristic(node)

    def heuristic(self, node):
        total = 0
        arr_goals = (self.room_fixed == 2)
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
        return total * self.penalty_for_step

    def back_propagate(self, result, node):
        while node is not None:
            node.utility = node.utility + result
            node.rollouts = node.rollouts + 1
            result += self.penalty_for_step
            node = node.parent

    def sensible_actions(self, player_position, room_state):
        def sensible(action, room_state, player_position):
            change = CHANGE_COORDINATES[action - 1] 
            new_pos = player_position + change
            #if the next pos is a wall
            if room_state[new_pos[0], new_pos[1]] == 0:
                return False
            new_box_position = new_pos + change
            # if a box is already at a wall
            if new_box_position[0] >= room_state.shape[0] \
                or new_box_position[1] >= room_state.shape[1]:
                    return False
            can_push_box = room_state[new_pos[0], new_pos[1]] in [3, 4]
            can_push_box &= room_state[new_box_position[0], new_box_position[1]] in [1, 2]
            if can_push_box:
                if self.room_fixed[new_box_position[0], new_box_position[1]] != 2:
                    box_surroundings_walls = []
                    for i in range(4):
                        surrounding_block = new_box_position + CHANGE_COORDINATES[i]
                        if room_state[surrounding_block[0], surrounding_block[1]] in [0,4]:
                            box_surroundings_walls.append(True)
                        else:
                            box_surroundings_walls.append(False)
                    wall_count = box_surroundings_walls.count(True) 
                    if wall_count >= 2:
                        if wall_count > 2:
                            return False
                        if not ((box_surroundings_walls[0] and box_surroundings_walls[1]) or (box_surroundings_walls[2] and box_surroundings_walls[3])):
                            return False
            return True
        return [action for action in self.actions if sensible(action, room_state, player_position)] 
    
CHANGE_COORDINATES = {
    0: (-1, 0),
    1: (1, 0),
    2: (0, -1),
    3: (0, 1)
}
