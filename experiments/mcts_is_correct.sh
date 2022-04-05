num_games=$1
timestamp=$(date +"%s")
log_file_name=${timestamp}_mcts_is_correct.txt
#Prueba que mcts es correcto
for time in 0.0001 0.0005 0.001 0.005 0.01 0.05 0.1
do 
    file=mcts${time}_greedy
    echo $file
    python3 ../simulation.py --teams mcts_$time greedy $num_games
done
