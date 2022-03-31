from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
from domino_mctspy import DominoGameState
import itertools
import random
from domino_state import DominoState, build_tiles
import collections
import sys
# random.seed(30)

def mcts_decision(state, num_simulations = None, total_simulation_seconds=1):
    root = TwoPlayersGameMonteCarloTreeSearchNode(state = DominoGameState(state))
    mcts = MonteCarloTreeSearch(root)
    return mcts.best_action(simulations_number=num_simulations, total_simulation_seconds=total_simulation_seconds).state._state

def random_combination(iterable, r):
    "Random selection from itertools.combinations(iterable, r)"
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.sample(range(n), r))
    return {pool[i] for i in indices}

def sample_combinations(iterable, r, sample_size):
    return [ random_combination(iterable, r) for i in range(sample_size)]

def sample_hands_uniformly(played_tiles, player_tiles,  num_tiles_by_player, sample_size):
    tiles = build_tiles()
    tiles_not_played = (tiles - played_tiles) - player_tiles
    first_hand_sample = sample_combinations(tiles_not_played,num_tiles_by_player[1], sample_size)
    second_hand_sample = [ random_combination(tiles_not_played - first_hand, num_tiles_by_player[2]) for first_hand in first_hand_sample]
    third_hand_sample = [ (tiles_not_played - first_hand_sample[i]) - second_hand_sample[i] for i in range(sample_size)]

    return first_hand_sample, second_hand_sample, third_hand_sample


def pimc_decision(suits_at_ends, my_tiles, played_tiles, num_tiles_by_player, sample_size=100, mcts_simulations=None, total_simulation_seconds=1):

    first_hand_sample, second_hand_sample, third_hand_sample = sample_hands_uniformly(played_tiles, my_tiles, num_tiles_by_player, sample_size)

    for i in range(sample_size):
        first_hand_sample[i] = [ set(tile) for tile in first_hand_sample[i]]
        second_hand_sample[i] = [ set(tile) for tile in second_hand_sample[i]]
        third_hand_sample[i] = [ set(tile) for tile in third_hand_sample[i]]


    decision_list = []
    my_tiles = [ set(tile) for tile in my_tiles]
    for i in range(sample_size):
        state = DominoState(0, {
            'tiles_by_player':[
                list(my_tiles),
                list(first_hand_sample[i]),
                list(second_hand_sample[i]),
                list(third_hand_sample[i])
            ],
            'suits_at_ends':suits_at_ends
        })
        decision_list.append(mcts_decision(state, num_simulations=mcts_simulations, total_simulation_seconds=total_simulation_seconds))

    decision_list = [ (frozenset(s.action.tile), s.action.suit_played) for s in decision_list]
    counter = collections.Counter(decision_list)
    tile, suit = counter.most_common(1)[0][0]
    return (set(tile), suit)

if __name__ == "__main__":
    tiles_by_player = [
        [{0}, {1, 2}, {1, 5}, {6}, {5, 6}, {4, 6}], 
        [{5},  {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
        [{4}, {3}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
        [{0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 4}, {1}]
    ] 
    assert(len(sys.argv) > 2)
    mcts_simulations = int(sys.argv[1])
    num_samples = int(sys.argv[2])
    played_tiles = {frozenset({4,5}), frozenset({5,2}), frozenset({2,3}), frozenset({3,6})}
    decision = pimc_decision(
        {4,6},
        { frozenset(tile) for tile in tiles_by_player[0]}, 
        played_tiles, 
        [len(tiles) for tiles in tiles_by_player],
        num_samples,
        mcts_simulations)
    print(decision)



    


    

