from utils import read_sokoban_input
from sokoban_env import SokobanEnv

if __name__ == '__main__':
    my_board = read_sokoban_input('sokoban00.txt')
    my_board.print()
