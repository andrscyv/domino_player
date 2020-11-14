from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
from domino import DominoGameState
from domino_state import deal_tiles, DominoState, DominoAction
import random

def play_mcts(state):
    root = TwoPlayersGameMonteCarloTreeSearchNode(state = DominoGameState(state))
    mcts = MonteCarloTreeSearch(root)
    return mcts.best_action(num_simulations).state._state

def play_greedy(state):
    actions = state.get_possible_actions()

    if len(actions) == 1:
        return state.next_state_from_action(actions[0])

    pips_of_actions = [ sum(action.tile) for action in actions ]
    index_of_greedy_action  = pips_of_actions.index(max(pips_of_actions))
    
    return state.next_state_from_action(actions[index_of_greedy_action]) 


if __name__ == "__main__":
    global num_simulations
    num_simulations = 1000
    tiles_by_player = deal_tiles()
    first_player = random.choice([0,1,2,3])
    state = DominoState(first_player, {
        'tiles_by_player': tiles_by_player,
        'suits_at_ends': set()
    })
    game = [state]

    while not state.is_terminal():
        if state._current_player in [0,2]:
            state = play_mcts(state)
        else:
            state = play_greedy(state)
        game.append(state)

    print(state.calc_reward())
    
