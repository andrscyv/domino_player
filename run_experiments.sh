mkdir ./experiments
num_games=$1

#Prueba que mcts es correcto
python3 simulation.py --simulations 1 --teams mcts greedy --file ./experiments/mcts1_greedy.pickle $num_games > ./experiments/mcts1_greedy.txt
file=mcts5_greedy
echo $file
python3 simulation.py --simulations 5 --teams mcts greedy --file ./experiments/$file.pickle $num_games > ./experiments/$file.txt
file=mcts_w_greedy
echo $file
python3 simulation.py --simulations 5 --teams mcts_w greedy --file ./experiments/$file.pickle $num_games > ./experiments/$file.txt
file=mcts_m_greedy
echo $file
python3 simulation.py --simulations 5 --teams mcts_m greedy --file ./experiments/$file.pickle $num_games > ./experiments/$file.txt
file=mcts_s_greedy
echo $file
python3 simulation.py --simulations 5 --teams mcts_s greedy --file ./experiments/$file.pickle $num_games > ./experiments/$file.txt
file=mcts_ss_greedy
echo $file
python3 simulation.py --simulations 5 --teams mcts_ss greedy --file ./experiments/$file.pickle $num_games > ./experiments/$file.txt

#Sensibilidad de mcts a num_simulations
file=mctsw_mctsss
echo $file
python3 simulation.py --simulations 5 --teams mcts_w mcts_ss --file ./experiments/$file.pickle $num_games > ./experiments/$file.txt
file=mctsm_mctsss
echo $file
python3 simulation.py --simulations 5 --teams mcts_m mcts_ss --file ./experiments/$file.pickle $num_games > ./experiments/$file.txt
file=mctss_mctsss
echo $file
python3 simulation.py --simulations 5 --teams mcts_s mcts_ss --file ./experiments/$file.pickle $num_games > ./experiments/$file.txt
file=mctsss_mctsss
echo $file
python3 simulation.py --simulations 5 --teams mcts_ss mcts_ss --file ./experiments/$file.pickle $num_games > ./experiments/$file.txt
file=mcts300_mctsss
echo $file
python3 simulation.py --simulations 300 --teams mcts mcts_ss --file ./experiments/$file.pickle $num_games > ./experiments/$file.txt

#Desempeño minimo
file=pimc20-100_greedy
echo $file
python3 simulation.py --simulations 20 --samples 100 --teams pimc greedy --file ./experiments/$file.pickle $num_games > ./experiments/$file.txt


 
