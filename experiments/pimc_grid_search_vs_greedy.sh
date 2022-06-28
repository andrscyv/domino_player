num_games=$1
timestamp=$(date +"%s")

num_samples_list=(500 1000 1500 2000 2500 3000 3500 4000 4500 5000 5500 6000 6500 7000 7500 8000 8500 9000 9500 10000)
time_budget_list=(0.00200 0.00100 0.00067 0.00050 0.00040 0.00033 0.00029 0.00025 0.00022 0.00020 0.00018 0.00017 0.00015 0.00014 0.00013 0.00013 0.00012 0.00011 0.00011 0.00010)
for idx in {1..$#num_samples_list}
do 
    num_samples=${num_samples_list[$idx]}
    time_budget=${time_budget_list[$idx]}
    echo $num_samples and $time_budget
    python3 ../simulation.py --teams pimc_${time_budget}_${num_samples} greedy $num_games 
done


 
