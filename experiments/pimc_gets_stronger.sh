num_games=$1

num_samples_list=(100  200  500  100  1000 100 2000 100 3000 100)
time_budget_list=(0.02 0.01 0.01 0.05 0.01 0.1 0.01 0.2 0.01 0.3)

for idx in {1..$#num_samples_list}
do 
    num_samples=${num_samples_list[$idx]}
    time_budget=${time_budget_list[$idx]}
    echo $num_samples and $time_budget
    python3 ../simulation.py --teams pimc_${time_budget}_${num_samples} greedy $num_games 
done


 
