from utils import parse
import gym
import gym_sokoban
import argparse
from mcts import MCTS
from time import time, sleep
from pathlib import Path

LEGAL_ACTIONS = [1,2,3,4]

ACTION_MAP = {
    'push up': "U",
    'push down': "D",
    'push left': "L",
    'push right': "R",
}

def mcts_solve(args, file):
    if args.render_mode == "raw":
        observation_mode = "raw"
    elif "tiny" in args.render_mode:
        observation_mode = "tiny_rgb_array"
    else:
        observation_mode = "rgb_array"
    dim_room, n_boxes, map = parse(filename= file)
    actions = []
    env = gym.make("MCTS-Sokoban-v0", dim_room=dim_room, num_boxes=n_boxes, original_map=map, max_steps=args.max_steps)
    solver = MCTS(env=env, max_rollouts=args.max_rollouts, max_depth=args.max_depth, actions=LEGAL_ACTIONS)
    allocated_time = args.time_limit * 60
    start_time = time()
    while True:
        now = time()
        if now - start_time > allocated_time:
            break
        env.render(mode=args.render_mode)
        observation, reward, done, info = solver.take_best_action(observation_mode=observation_mode)
        if "action.name" in info:            
            actions.append(ACTION_MAP[info["action.name"]])
        if done and "mcts_giveup" in info:
            env.reset()
            actions.clear()
        elif done and info["all_boxes_on_target"]:
            actions.append("Solved in {:.0f} mins".format((now - start_time)/60))
            break
        elif done and info["maxsteps_used"]:
            env.reset()
            actions.clear()
    env.render(mode=args.render_mode)
    sleep(3)
    env.close()
    log_dir = Path(args.log_dir)
    log_dir.mkdir(exist_ok=True)
    with open(log_dir / "{}.log".format(file.stem), mode="w") as log:
        print("{}".format(len(actions)), file=log, end="")
        for action in actions:
            print(" {}".format(action), file=log, end="")
    
def main(args):
    if args.file:
        for file in args.file:
            mcts_solve(args, Path(file))
    else:
        for file in Path(args.folder).iterdir():
            mcts_solve(args, file)
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", nargs = "+", help= "file that defines the sokoban map")
    group.add_argument("--folder", help= "folder that contains files which define the sokoban map")
    parser.add_argument("--render_mode", help="Obversation mode for the game. Use human to see a render on the screen", default="raw")
    parser.add_argument("--max_rollouts", type=int, help="Number of rollouts per move", default=4000)
    parser.add_argument("--max_depth", type=int, help="Depth of each rollout", default=30)
    parser.add_argument("--max_steps", type=int, help="Max moves before game is lost", default=120)
    parser.add_argument("--time_limit", type=int, help="Allocated Time (in minutes) per board", default=60)
    parser.add_argument("--log_dir", type=str, help="Directory to log solve information", default="./solve_log")
    args = parser.parse_args()
    main(args)
    
