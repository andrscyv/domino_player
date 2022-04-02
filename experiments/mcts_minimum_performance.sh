num_games=$1
timestamp=$(date +"%s")
log_file_name=${timestamp}_minimun_performance.txt
time=0.01
num_samples=100
#Desempeño minimo
file=pimc${time}-${num_samples}_greedy
echo $file
python3 ../simulation.py --time-budget $time --samples $num_samples --teams pimc greedy --file ./pickles/${timestamp}_$file.pickle $num_games >> ./logs/$log_file_name



 
