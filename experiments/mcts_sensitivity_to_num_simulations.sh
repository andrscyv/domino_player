#!/bin/zsh

num_games=$1
strong_player_time_budget=1

for idx in {1..$#time_budget_list}
do 
    time=${time_budget_list[$idx]}
    players=mcts${time}_mcts$strong_player_time_budget
    printf "%-20s for %d games \n" $players $num_games 
    python3 ../simulation.py --teams mcts_$time mcts_$strong_player_time_budget $num_games 
done


 
