from utils import parse
import gym
import gym_sokoban
import argparse
from mcts import MCTS
from time import time, sleep
from pathlib import Path

LEGAL_ACTIONS = [1,2,3,4]

def mcts_solve(args, file):
    if args.render_mode == "raw":
        observation_mode = "raw"
    elif "tiny" in args.render_mode:
        observation_mode = "tiny_rgb_array"
    else:
        observation_mode = "rgb_array"
    log_dir = Path(args.log_dir)
    log_dir.mkdir(exist_ok=True)
    log = open(log_dir / "{}.log".format(file.stem), mode="w")
    dim_room, n_boxes, map = parse(filename= file)
    env = gym.make("MCTS-Sokoban-v0", dim_room=dim_room, num_boxes=n_boxes, original_map=map, max_steps=args.max_steps)
    solver = MCTS(env=env, max_rollouts=args.max_rollouts, max_depth=args.max_depth, actions=LEGAL_ACTIONS)
    allocated_time = args.time_per_board * 60
    start_time = time()
    i = 0
    while True:
        now = time()
        if now - start_time > allocated_time:
            print("MCTS couldn't solve {} in allocated time.".format(file.name), file=log)
            break
        env.render(mode=args.render_mode)
        observation, reward, done, info = solver.take_best_action(observation_mode=observation_mode)
        i += 1
        print(info, file=log)
        if done and "mcts_giveup" in info:
            env.reset()
            i = 0
        elif done and info["maxsteps_used"]:
            print("All steps used. Resetting board.", file=log)
            env.reset()
            i = 0
        elif done and info["all_boxes_on_target"]:
            print("Solved {} after {} steps.".format(file.name, i), file=log)
            break
        log.flush()
    log.close()
    env.render(mode=args.render_mode)
    sleep(3)
    env.close()

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
    parser.add_argument("--render_mode", help="Obversation mode for the game", default="human")
    parser.add_argument("--max_rollouts", type=int, help="Number of rollouts per move", default=350)
    parser.add_argument("--max_depth", type=int, help="Depth of each rollout", default=10)
    parser.add_argument("--max_steps", type=int, help="Max moves before game is lost", default=120)
    parser.add_argument("--time_per_board", type=int, help="Allocated Time (in minutes) per board", default=60)
    parser.add_argument("--log_dir", type=str, help="Directory to log solve information", default="./solve_log")
    args = parser.parse_args()
    main(args)
    
