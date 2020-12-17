mkdir ./experiments2
num_games=$1

#Sensibilidad pimc
file=pimc1-100_greedy
echo $file
python3 simulation.py --simulations 1 --samples 100 --teams pimc greedy --file ./experiments2/$file.pickle $num_games > ./experiments2/$file.txt
file=pimc5-100_greedy
echo $file
python3 simulation.py --simulations 5 --samples 100 --teams pimc greedy --file ./experiments2/$file.pickle $num_games > ./experiments2/$file.txt
file=pimc60-100_greedy
echo $file
python3 simulation.py --simulations 60 --samples 100 --teams pimc greedy --file ./experiments2/$file.pickle $num_games > ./experiments2/$file.txt
file=pimc100-100_greedy
echo $file
python3 simulation.py --simulations 100 --samples 100 --teams pimc greedy --file ./experiments2/$file.pickle $num_games > ./experiments2/$file.txt
file=pimc200-100_greedy
echo $file
python3 simulation.py --simulations 200 --samples 100 --teams pimc greedy --file ./experiments2/$file.pickle $num_games > ./experiments2/$file.txt


file=pimc20-10_greedy
echo $file
python3 simulation.py --simulations 20 --samples 10 --teams pimc greedy --file ./experiments2/$file.pickle $num_games > ./experiments2/$file.txt
file=pimc20-60_greedy
echo $file
python3 simulation.py --simulations 20 --samples 60 --teams pimc greedy --file ./experiments2/$file.pickle $num_games > ./experiments2/$file.txt
file=pimc20-150_greedy
echo $file
python3 simulation.py --simulations 20 --samples 150 --teams pimc greedy --file ./experiments2/$file.pickle $num_games > ./experiments2/$file.txt
file=pimc20-200_greedy
echo $file
python3 simulation.py --simulations 20 --samples 200 --teams pimc greedy --file ./experiments2/$file.pickle $num_games > ./experiments2/$file.txt



file=pimc20-100_mctss
echo $file
python3 simulation.py --simulations 20 --samples 100 --teams pimc mcts_s --file ./experiments2/$file.pickle $num_games > ./experiments2/$file.txt
 
