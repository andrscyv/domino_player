mkdir ./experiments
num_games=100
python3 simulation.py --simulations 1 --teams mcts greedy --file ./experiments/mcts1_greedy.pickle $num_games > ./experiments/mcts1_greedy.txt

