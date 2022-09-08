num_games=$1
# Optimal parameters for pimc found by grid search
time=0.01333
num_samples=75
#Desempeño minimo
players=pimc${time}-${num_samples}_greedy
echo $players
python3 ../simulation.py --teams pimc_${time}_${num_samples} greedy $num_games



 
