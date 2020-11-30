from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
from domino import DominoGameState
import itertools
import random
from domino_state import DominoState, build_tiles
import collections
random.seed(30)

def mcts_decision(state, num_simulations = 100):
    root = TwoPlayersGameMonteCarloTreeSearchNode(state = DominoGameState(state))
    mcts = MonteCarloTreeSearch(root)
    return mcts.best_action(num_simulations).state._state

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
    first_hand_sample = sample_combinations(tiles_not_played,num_tiles_by_player[0], sample_size)
    second_hand_sample = [ random_combination(tiles_not_played - first_hand, num_tiles_by_player[1]) for first_hand in first_hand_sample]
    third_hand_sample = [ first_hand_sample[i] - second_hand_sample[i] for i in range(sample_size)]

    return first_hand_sample, second_hand_sample, third_hand_sample


def pimc_decision(suits_at_ends, my_tiles, played_tiles, num_tiles_by_player, sample_size=100, mcts_simulations=100):

    first_hand_sample, second_hand_sample, third_hand_sample = sample_hands_uniformly(played_tiles, my_tiles, num_tiles_by_player, sample_size)

    for i in range(sample_size):
        first_hand_sample[i] = [ set(tile) for tile in first_hand_sample[i]]
        second_hand_sample[i] = [ set(tile) for tile in second_hand_sample[i]]
        third_hand_sample[i] = [ set(tile) for tile in third_hand_sample[i]]


    decision_list = []
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
        decision_list.append(mcts_decision(state, mcts_simulations))

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
    played_tiles = {frozenset({4,5}), frozenset({5,2}), frozenset({2,3}), frozenset({3,6})}
    decision = pimc_decision(
        {4,6},
        tiles_by_player[0], 
        played_tiles, 
        [len(tiles) for tiles in tiles_by_player],
        100)
    print(decision)



    


    

