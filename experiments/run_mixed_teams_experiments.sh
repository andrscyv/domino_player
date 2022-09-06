num_games=$1

# Optimal parameters for pimc found by grid search
time=0.01333
num_samples=75

source pimc_weak_vs_weak_weak.sh $1 && \
source pimc_strong_vs_weak_weak.sh $1 && \
source pimc_weak_vs_strong_strong.sh $1 && \
source pimc_strong_vs_strong_strong.sh $1 