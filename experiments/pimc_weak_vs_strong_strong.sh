echo pimc_greedy vs mcts1_mcts1
pimc=pimc_${time}_${num_samples} 
python3 ../simulation.py --players $pimc mcts_1 greedy mcts_1 $num_games