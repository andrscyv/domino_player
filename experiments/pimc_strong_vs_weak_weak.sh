echo pimc_mcts_1 vs greedy_greedy
pimc=pimc_${time}_${num_samples} 
python3 ../simulation.py --players $pimc greedy mcts_1 greedy $num_games
