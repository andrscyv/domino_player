echo pimc_greedy vs greedy_greedy
pimc=pimc_${time}_${num_samples} 
python3 ../simulation.py --players $pimc greedy greedy greedy $num_games
