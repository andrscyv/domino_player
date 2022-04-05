num_games=$1
timestamp=$(date +"%s")
log_file_name=${timestamp}_mcts_sensitivity_to_num_simulations.txt
strong_player_time_budget=0.1

for time in 0.0001 0.0005 0.001 0.005 0.01 0.05 0.1 0.5 1 1.5 2 2.5 3 3.5 4 4.5 5
do 
    file=mcts${time}_mcts$strong_player_time_budget
    echo $file
    python3 ../simulation.py --teams mcts_$time mcts_$strong_player_time_budget $num_games 
done


 
