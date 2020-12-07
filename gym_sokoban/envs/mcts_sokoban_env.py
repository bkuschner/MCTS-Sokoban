import numpy as np
from .sokoban_env import SokobanEnv
from .render_utils import room_to_rgb
import copy

class MCTSSokobanEnv(SokobanEnv):
    # format of coordinates is (row, column) 1-indexed
    # @param size: a list with num columns and num rows
    # @param walls: a set of tuples each containing coordinates of walls
    # @param walls: a set of tuples each containing coordinates of boxes
    # @param walls: a set of tuples each containing coordinates of storage
    # @param start: a tuple containing coordinates of start space
    def __init__(self, dim_room, num_boxes, original_map, max_steps=120):
        self.original_map = original_map
        super(MCTSSokobanEnv, self).__init__(dim_room, max_steps, num_boxes, None)

    def reset(self):
        self.room_fixed, self.room_state, self.box_mapping = self.generate_room(self.original_map)
        self.num_env_steps = 0
        self.reward_last = 0
        self.boxes_on_target = 0
        starting_observation = room_to_rgb(self.room_state, self.room_fixed)
        return starting_observation
            
    def generate_room(self, select_map):
        room_fixed = []
        room_state = []

        targets = []
        boxes = []
        for row in select_map:
            room_f = []
            room_s = []

            for e in row:
                if e == '#':
                    room_f.append(0)
                    room_s.append(0)

                elif e == '@':
                    self.player_position = np.array([len(room_fixed), len(room_f)])
                    room_f.append(1)
                    room_s.append(5)


                elif e == '$':
                    boxes.append((len(room_fixed), len(room_f)))
                    room_f.append(1)
                    room_s.append(4)

                elif e == '.':
                    targets.append((len(room_fixed), len(room_f)))
                    room_f.append(2)
                    room_s.append(2)

                else:
                    room_f.append(1)
                    room_s.append(1)

            room_fixed.append(room_f)
            room_state.append(room_s)


        # used for replay in room generation, unused here because pre-generated levels
        box_mapping = {}

        return np.array(room_fixed), np.array(room_state), box_mapping
    
    def simulate_step(self, action, state):
        boxes_on_target, num_env_steps, player_position, room_state = state
        self.backup_env_states()
        self.room_state = room_state
        self.player_position = player_position
        self.boxes_on_target = boxes_on_target
        self.num_env_steps = num_env_steps
        observation, reward_last, done, info = self.step(action, observation_mode="raw")
        new_boxes_on_target = self.boxes_on_target
        new_num_env_steps = self.num_env_steps
        new_player_position = self.player_position
        new_room_state = self.room_state
        self.restore_env_states()
        return (new_boxes_on_target, new_num_env_steps, new_player_position, new_room_state), observation, reward_last, done, info
    
    def backup_env_states(self):
        self.reward_last_backup = copy.deepcopy(self.reward_last)
        self.boxes_on_target_backup = copy.deepcopy(self.boxes_on_target)
        self.num_env_steps_backup = copy.deepcopy(self.num_env_steps)
        self.player_position_backup = copy.deepcopy(self.player_position)
        self.room_state_backup = copy.deepcopy(self.room_state)
        
    def restore_env_states(self):
        self.reward_last = self.reward_last_backup
        self.boxes_on_target = self.boxes_on_target_backup
        self.num_env_steps = self.num_env_steps_backup
        self.player_position = self.player_position_backup
        self.room_state = self.room_state_backup