import pickle, calendar, time
import click
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import math


def save_games_played(simulation_params, games, file_path):
    if not file_path:
        file_path = f"./simulations/{calendar.timegm(time.gmtime())}"

    with open(file_path,'wb') as f:
        pickle.dump((simulation_params, games), f)
        
def load_games(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def collect_stats(games):
    accum_plays_per_turn = [0]*40
    num_of_turns_observed = [0]*40
    accum_game_length = 0
    num_of_games = len(games)
    plays_per_turn = np.zeros((num_of_games,40))
    
    for (i,game)  in enumerate(games):
        for (k, state) in enumerate(game):
            num_of_actions =  len(state.get_possible_actions())
            accum_plays_per_turn[k] += num_of_actions 
            plays_per_turn[i,k] = num_of_actions
            num_of_turns_observed[k] += 1
        
        accum_game_length += len(game)

    return (accum_game_length/num_of_games, plays_per_turn)

def graphs(plays_per_turn):
    n = plays_per_turn.shape[0]
    alpha = 0.05
    print(n)
    t_quantile = stats.t(df=(n-1)).ppf(1-alpha/2)
    print(t_quantile)
    mean = np.mean(plays_per_turn, axis=0)
    std = np.std(plays_per_turn, axis=0)
    yerr = t_quantile*std/math.sqrt(n)
    x = np.arange(len(mean))
    plt.errorbar(x,mean, yerr=std )
    plt.ylabel('Acciones posibles')
    plt.xlabel('Turno')
    plt.title('Factor de ramificación promedio')
    plt.show()


@click.command()
@click.argument('file_path', type=click.Path(exists=True) )
def run(file_path):
    games = load_games(file_path)
    print(games[0])
    print('Num games', len(games[1]))
    print('Longest game', max([len(game) for game in games[1]]))
    avg_game_lenght, plays_per_turn = collect_stats(games[1])
    print(F"Avg game length: {avg_game_lenght}")
    print(F"Avg branching factor:  {np.mean(plays_per_turn[:,:36])}")
    print(F"Std branching factor:  {np.std(plays_per_turn[:,:23])}")
    graphs(plays_per_turn)


if __name__ == "__main__":
    run()


