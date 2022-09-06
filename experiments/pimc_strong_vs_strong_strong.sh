echo pimc_mcts1 vs mcts1_mcts1
pimc=pimc_${time}_${num_samples} 
python3 ../simulation.py --players $pimc mcts_1 mcts_1 mcts_1 $num_games