num_games=$1
#Prueba que mcts es correcto

for idx in {1..$#time_budget_list}
do 
    time=${time_budget_list[$idx]}
    players=mcts${time}_greedy
    printf "%-20s for %d games \n" $players $num_games 
    python3 ../simulation.py --teams mcts_$time greedy $num_games
done
