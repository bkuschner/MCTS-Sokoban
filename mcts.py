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
    def __init__(self, env, max_rollouts = 4000, max_depth = 30, actions = [1,2,3,4], verbose = False):
        self.env = env
        self.step = 0
        self.max_rollouts = max_rollouts
        self.max_depth = max_depth
        self.actions = actions
        self.penalty_for_step = env.penalty_for_step
        self.reward_finished = env.reward_finished + env.reward_box_on_target
        self.num_boxes= env.num_boxes
        self.room_fixed = env.room_fixed
        self.last_pos = env.player_position
        self.moved_box = True
        self.verbose = verbose
        
    def take_best_action(self, observation_mode="rgb_array"):
        env_state = self.env.get_current_state()
        best_action = self.mcts(env_state)
        #if mcts couldn't find a sensible move from this position
        if best_action == -1:
            return None, -1, True, {"mcts_giveup": "MCTS Gave up, board unsolvable. Reset board"}
        observation, reward, done, info = self.env.step(best_action, observation_mode=observation_mode)
        self.last_pos = env_state[2]
        self.moved_box = info["action.moved_box"]
        return observation, reward, done, info

    def mcts(self, env_state):
        root = Node("0",env_state, last_pos=self.last_pos, move_box=self.moved_box)
        rollouts = 0
        while rollouts <= self.max_rollouts:
            child, immediate_reward = self.select_and_expand(root)
            #Board is unsolvable, if child is the root
            if child.parent == None:
                return -1
            result = self.simulate(child, immediate_reward)
            self.back_propagate(result, child)
            rollouts += 1

        # find and return the action that got rolled out the most
        if self.verbose:
            for pre, fill, node in RenderTree(root):
                treestr = u"%s%s" % (pre, node.name)
                print(treestr.ljust(8), node.utility/ node.rollouts, node.rollouts)
        best_child = max(root.children, key= lambda child: child.rollouts)

        return best_child.action

    def select_and_expand(self, tree):
        while not tree.done:
            sensible_actions = self.sensible_actions(tree.state[2], tree.state[3], tree.last_pos, tree.move_box)
            if len([child.action for child in tree.children]) < len(sensible_actions):
                return self.expand(tree, sensible_actions)
            elif len(sensible_actions) == 0:
                return tree, -self.reward_finished
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
        new_child = Node(name=node.name +"-{}".format(action) , state=state, last_pos= node.state[2], move_box = info["action.moved_box"], done=done, parent=node, action=action)
        return new_child, reward_last

    def ucb_select(self, tree):
        best_child = max(tree.children, key = lambda child: ((child.utility / child.rollouts) + (sqrt(2) * log(tree.rollouts) / child.rollouts)))
        return best_child

    def simulate(self, node, immediate_reward):
        depth = 0
        total_reward = immediate_reward
        state = node.state
        done = node.done
        last_pos = node.last_pos
        move_box = node.move_box
        while not done and depth < self.max_depth:
            possible_actions = self.sensible_actions(state[2], state[3], last_pos, move_box)
            if not possible_actions:
                break
            action = random.choice(possible_actions)
            new_state, observation, reward, done, info = self.env.simulate_step(action=action, state=state)
            last_pos = state[2]
            move_box = info["action.moved_box"]
            state = new_state
            total_reward += reward
            depth += 1
        return total_reward + self.heuristic(state[3])

    def heuristic(self, room_state):
        total = 0
        arr_goals = (self.room_fixed == 2)
        arr_boxes = ((room_state == 4) + (room_state == 3))
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
            node.utility += result
            node.rollouts += 1
            result += self.penalty_for_step
            node = node.parent

    def sensible_actions(self, player_position, room_state, last_pos, move_box):
        def sensible(action, room_state, player_position, last_pos, move_box):
            change = CHANGE_COORDINATES[action - 1] 
            new_pos = player_position + change
            #if the next pos is a wall
            if room_state[new_pos[0], new_pos[1]] == 0:
                return False
            if np.array_equal(new_pos, last_pos) and not move_box:
                return False
            new_box_position = new_pos + change
            # if a box is already at a wall
            if new_box_position[0] >= room_state.shape[0] \
                or new_box_position[1] >= room_state.shape[1]:
                    return False
            can_push_box = room_state[new_pos[0], new_pos[1]] in [3, 4]
            can_push_box &= room_state[new_box_position[0], new_box_position[1]] in [1, 2]
            if can_push_box:
                #check if we are pushing a box into a corner
                if self.room_fixed[new_box_position[0], new_box_position[1]] != 2:
                    box_surroundings_walls = []
                    for i in range(4):
                        surrounding_block = new_box_position + CHANGE_COORDINATES[i]
                        if self.room_fixed[surrounding_block[0], surrounding_block[1]] == 0:
                            box_surroundings_walls.append(True)
                        else:
                            box_surroundings_walls.append(False)
                    if box_surroundings_walls.count(True) >= 2:
                        if box_surroundings_walls.count(True) > 2:
                            return False
                        if not ((box_surroundings_walls[0] and box_surroundings_walls[1]) or (box_surroundings_walls[2] and box_surroundings_walls[3])):
                            return False
            # trying to push box into wall
            if room_state[new_pos[0], new_pos[1]] in [3, 4] and room_state[new_box_position[0], new_box_position[1]] not in [1, 2]:
                return False
            return True
        return [action for action in self.actions if sensible(action, room_state, player_position, last_pos, move_box)] 
    
CHANGE_COORDINATES = {
    0: (-1, 0),
    1: (1, 0),
    2: (0, -1),
    3: (0, 1)
}
