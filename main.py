from utils import parse
import gym
import gym_sokoban

if __name__ == '__main__':
    dim_room, n_boxes, map = parse("sokoban00.txt")
    env = gym.make("MCTS-Sokoban-v0", dim_room=dim_room, n_boxes=n_boxes, map=map)
    
