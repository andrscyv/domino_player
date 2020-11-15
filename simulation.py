from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
from domino import DominoGameState
from domino_state import deal_tiles, DominoState, DominoAction
import random
import pprint

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

def print_state(state):
    if not state.action:
        return

    print(f"\nPlayer: {state.action.player} {state.action.tile} suits: {state._suits_at_ends}")

def play_game():
    tiles_by_player = deal_tiles()
    first_player = random.choice([0,1,2,3])
    state = DominoState(first_player, {
        'tiles_by_player': tiles_by_player,
        'suits_at_ends': set()
    })
    # game = [state]
    # pp = pprint.PrettyPrinter()
    # print(f"Starts player {first_player}" )
    # pp.pprint(state._tiles_by_player)
    while not state.is_terminal():
        # print("=======================================")
        # pp.pprint(state._tiles_by_player[state._current_player])
        if state._current_player in [0,2]:
            state = play_mcts(state)
        else:
            state = play_greedy(state)
        # game.append(state)
        # print_state(state)
    # print("winneeeer", state.calc_reward())
    # pp.pprint(state._tiles_by_player)

    return state.calc_reward()


if __name__ == "__main__":
    global num_simulations
    num_simulations = 500
    game_results = []
    for i in range(100):
        game_results.append(play_game())
        print(i)

    print(f"Porcentaje ganado {sum([result for result in game_results if result == 1])/len(game_results)}")





    
