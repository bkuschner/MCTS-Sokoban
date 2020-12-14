# MCTS-Sokoban
A Sokoban solver using Monte Carlo Tree Search. 

To quickly execute the solver, run the commands "pip install -e ." and "python main.py --folder ./boards" 

This version of the environment extends the popular gym environment for sokoban and adds a mcts_sokoban version of the environment to work with the project inputs and add a few functions for monte carlo tree search. Refer back to https://github.com/mpSchrader/gym-sokoban for the details on the original environment. 

Execute the solver by calling main.py with the argument --file to attempt to solve the provided file path(es). To execute the solve on a folder, simply provide the folder path with the --folder argument. By default, the output is stored in "solve_log/[input file name].log" and the environment renders are not shown. To see a render of the gym environment, use "human" as the argument to --render_mode. To change the solve time limit set for each board, use the --time_limit argument.