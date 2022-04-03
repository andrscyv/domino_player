#!/bin/bash

# nohup ./run_experiments.sh $1 &
# echo $! > pid.txt

source run_experiment.sh mcts_is_correct.sh $1 && \
source run_experiment.sh mcts_minimum_performance.sh $1 && \
source run_experiment.sh mcts_sensitivity_to_num_simulations.sh $1

