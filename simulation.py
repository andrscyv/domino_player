from domino_easyai import GameOfDomino
from easyAI import Human_Player, AI_Player, Negamax
from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
from domino_mctspy import DominoGameState
from domino_state import deal_tiles, DominoState, DominoAction
import random
from pprint import pformat
from pimc import pimc_decision
import sys

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


def play_pimc(state, game):

    def rotate(l, n):
        return l[n:] + l[:n]

    played_tiles = { frozenset(s.action.tile) for s in game}
    my_tiles = { frozenset(tile) for tile in state._tiles_by_player[state._current_player]}
    num_tiles_by_player = [len(tiles) for tiles in rotate(state._tiles_by_player,state._current_player)]
    tile, suit_played = pimc_decision(
        state._suits_at_ends,
        my_tiles,
        played_tiles,
        num_tiles_by_player,
        10,
        300
    )

    return state.next_state_from_action(DominoAction(state._current_player, tile, suit_played))

def play_perfect(state):
    ai = Negamax(28)
    easy_ai = GameOfDomino([AI_Player(ai), Human_Player()])
    easy_ai._state = state
    move = easy_ai.get_move()
    easy_ai.play_move(move)

    return easy_ai._state

def print_state(state):
    if not state.action:
        return

    log(f"\nPlayer: {state.action.player} {state.action.tile} suits: {state._suits_at_ends}")

def log(message):
    if debug:
        print(message)

def play_game():
    tiles_by_player = deal_tiles()
    first_player = random.choice([0,1,2,3])
    state = DominoState(first_player, {
        'tiles_by_player': tiles_by_player,
        'suits_at_ends': set()
    })
    game = [state]
    log(f"Starts player {first_player}" )
    log("Tiles : " )
    log(pformat(state._tiles_by_player))
    game = []
    while not state.is_terminal():
        log("=======================================")
        log(pformat(state._tiles_by_player[state._current_player]))
        if state._current_player in [0,2]:
            # state = play_mcts(state)
            # state = play_pimc(state, game)
            state = play_perfect(state)
        else:
            state = play_greedy(state)
        game.append(state)
        print_state(state)
    log(f"winneeeer {state.calc_reward()}")
    log(pformat(state._tiles_by_player))

    return state.calc_reward()


if __name__ == "__main__":
    global num_simulations
    global debug
    # random.seed(30)
    assert(len(sys.argv) > 2)
    num_simulations = int(sys.argv[1])
    num_games = int(sys.argv[2])
    debug = True
    # players = sys.argv[3:7]
    game_results = []
    for i in range(num_games):
        print(f'... game {i}')
        game_results.append(play_game())

    print(f"Porcentaje ganado {sum([result for result in game_results if result == 1])/len(game_results)}")





    
