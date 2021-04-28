mkdir ./experiments
mkdir ./experiments_logs
num_games=$1
timestamp=$(date +"%s")
log_file_name=${timestamp}_mcts_is_correct.txt
#Prueba que mcts es correcto
for time in 0.0001 0.0005 0.001 0.005 0.01 0.05 0.1
do 
    file=mcts${time}_greedy
    echo $file
    python3 simulation.py --time-budget $time --teams mcts greedy --file ./experiments/${timestamp}_$file.pickle $num_games >> ./experiments_logs/$log_file_name
done


# #Sensibilidad de mcts a num_simulations
# file=mctsw_mctsss
# echo $file
# python3 simulation.py --simulations 5 --teams mcts_w mcts_ss --file ./experiments/$file.pickle $num_games > ./experiments/$file.txt
# file=mctsm_mctsss
# echo $file
# python3 simulation.py --simulations 5 --teams mcts_m mcts_ss --file ./experiments/$file.pickle $num_games > ./experiments/$file.txt
# file=mctss_mctsss
# echo $file
# python3 simulation.py --simulations 5 --teams mcts_s mcts_ss --file ./experiments/$file.pickle $num_games > ./experiments/$file.txt
# file=mctsss_mctsss
# echo $file
# python3 simulation.py --simulations 5 --teams mcts_ss mcts_ss --file ./experiments/$file.pickle $num_games > ./experiments/$file.txt
# file=mcts300_mctsss
# echo $file
# python3 simulation.py --simulations 300 --teams mcts mcts_ss --file ./experiments/$file.pickle $num_games > ./experiments/$file.txt

# #Desempeño minimo
# file=pimc20-100_greedy
# echo $file
# python3 simulation.py --simulations 20 --samples 100 --teams pimc greedy --file ./experiments/$file.pickle $num_games > ./experiments/$file.txt


 
