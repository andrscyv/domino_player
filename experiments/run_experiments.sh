#!/bin/bash

# nohup ./run_experiments.sh $1 &
# echo $! > pid.txt

# declare an array of time budgets from 0.0001 to 0.05 in steps of 0.0001
# time_budget_list=(0.0001 0.0005 0.001 0.005 0.01 0.05 0.1 0.5 1 1.5 2 2.5 3 3.5 4 4.5 5)
time_budget_list=(1 0.04 0.02 0.01333 0.01 0.008 0.00666 0.00571 0.005 0.00444 0.004 0.00363 0.00333 0.00307 0.00285 0.00266 0.0025 0.00235 0.00222 0.0021 0.002)

source mcts_is_correct.sh $1 && \
source mcts_minimum_performance.sh $1 && \
source mcts_sensitivity_to_num_simulations.sh $1

