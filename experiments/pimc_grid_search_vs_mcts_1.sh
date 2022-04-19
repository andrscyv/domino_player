num_games=$1
timestamp=$(date +"%s")

num_samples_list=(10000 2000 1000 200 100 20 10 2 1)
time_budget_list=(0.0001 0.0005 0.001 0.005 0.01 0.05 0.1 0.5 1)
for idx in {1..$#num_samples_list}
do 
    num_samples=${num_samples_list[$idx]}
    time_budget=${time_budget_list[$idx]}
    echo $num_samples and $time_budget
    python3 ../simulation.py --teams pimc_${time_budget}_${num_samples} mcts_1 $num_games 
done


 
