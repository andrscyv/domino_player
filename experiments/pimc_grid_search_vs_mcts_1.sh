num_games=$1
timestamp=$(date +"%s")

for idx in {1..$#num_samples_list}
do 
    num_samples=${num_samples_list[$idx]}
    time_budget=${time_budget_list[$idx]}
    echo $num_samples and $time_budget
    python3 ../simulation.py --teams pimc_${time_budget}_${num_samples} mcts_1 $num_games 
done


 
