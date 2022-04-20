#!/bin/zsh

# nohup ./run_experiments.sh $1 &
# echo $! > pid.txt

source run_experiment.sh pimc_grid_search_vs_greedy.sh $1 && \
source run_experiment.sh pimc_grid_search_vs_mcts_1.sh $1

