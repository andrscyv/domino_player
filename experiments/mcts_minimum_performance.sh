num_games=$1
time=0.01
num_samples=100
#Desempeño minimo
players=pimc${time}-${num_samples}_greedy
echo $players
python3 ../simulation.py --teams pimc_${time}_${num_samples} greedy $num_games



 
