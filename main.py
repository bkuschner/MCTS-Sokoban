from utils import parse
import gym
import gym_sokoban
import argparse
from mcts import MCTS

LEGAL_ACTIONS = [1,2,3,4]

def main(args):
    dim_room, n_boxes, map = parse(filename= args.file)
    if args.render_mode == "raw":
        observation_mode = "raw"
    elif "tiny" in args.render_mode:
        observation_mode = "tiny_rgb_array"
    else:
        observation_mode = "rgb_array"
    env = gym.make("MCTS-Sokoban-v0", dim_room=dim_room, n_boxes=n_boxes, map=map, max_steps=args.max_steps)
    solver = MCTS(env=env, max_rollouts=args.max_mcts_rollouts, max_depth=args.max_mcts_depth, actions=LEGAL_ACTIONS)
    for i in range(args.max_steps):
        env.render(mode=args.render_mode)
        observation, reward, done, info = solver.take_best_action(observation_mode=observation_mode)
        print(info, reward)
        if done:
            "Solved after {} steps".format(i+1)
            break
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help= "file that defines the sokoban map", required= True)
    parser.add_argument("--render_mode", help="Obversation mode for the game", default="human")
    parser.add_argument("--max_mcts_rollouts", type=int, help="Number of rollouts per move", default=10000)
    parser.add_argument("--max_mcts_depth", type=int, help="Depth of each rollout", default=30)
    parser.add_argument("--max_steps", type=int, help="Max moves before game is lost", default=120)
    args = parser.parse_args()
    main(args)
    
