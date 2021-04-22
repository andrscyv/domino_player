from domino_easyai import GameOfDomino
from easyAI import Human_Player, AI_Player, Negamax
from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
from domino_mctspy import DominoGameState
from domino_state import deal_tiles, DominoState, DominoAction
import random
from pprint import pformat
from pimc import pimc_decision
from stats import save_games_played
import click

def play_mcts(state, num_simulations=None, total_simulation_seconds=1):
    current_player = state._current_player
    tiles_by_player = state._tiles_by_player
    aux_state = DominoState(0, {
        'tiles_by_player': rotate(tiles_by_player, current_player),
        'suits_at_ends': state._suits_at_ends
    })
    root = TwoPlayersGameMonteCarloTreeSearchNode(state = DominoGameState(aux_state))
    mcts = MonteCarloTreeSearch(root)
    best_action = mcts.best_action(simulations_number=num_simulations, total_simulation_seconds=total_simulation_seconds).state._state.action
    return state.next_state_from_action(DominoAction(current_player, best_action.tile, best_action.suit_played))

def play_greedy(state):
    actions = state.get_possible_actions()

    if len(actions) == 1:
        return state.next_state_from_action(actions[0])

    pips_of_actions = [ sum(action.tile) for action in actions ]
    index_of_greedy_action  = pips_of_actions.index(max(pips_of_actions))
    
    return state.next_state_from_action(actions[index_of_greedy_action]) 

def rotate(l, n):
    return l[n:] + l[:n]

def play_pimc(state, game, num_samples, num_simulations=None, total_simulation_seconds=1 ):


    played_tiles = { frozenset(s.action.tile) for s in game[1:]}
    my_tiles = { frozenset(tile) for tile in state._tiles_by_player[state._current_player]}
    num_tiles_by_player = [len(tiles) for tiles in rotate(state._tiles_by_player,state._current_player)]
    tile, suit_played = pimc_decision(
        state._suits_at_ends,
        my_tiles,
        played_tiles,
        num_tiles_by_player,
        num_samples, 
        mcts_simulations=num_simulations,
        total_simulation_seconds=total_simulation_seconds
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

def play_with_algo(algo, state, game, num_samples, num_simulations=None, total_simulation_seconds=1):
    if algo == 'mcts':
        return play_mcts(state, num_simulations=num_simulations, total_simulation_seconds=total_simulation_seconds)

    if algo == 'greedy':
        return play_greedy(state)

    if algo == 'pimc':
        return play_pimc(state, game, num_samples, num_simulations=num_simulations, total_simulation_seconds=total_simulation_seconds)

    if algo == 'mcts_w':
        return play_mcts(state, 20)
        
    if algo == 'mcts_m':
        return play_mcts(state, 60)
        
    if algo == 'mcts_s':
        return play_mcts(state, 100)
        
    if algo == 'mcts_ss':
        return play_mcts(state, 250)
        

def play_game(players, num_samples=100, num_simulations=None, total_simulation_seconds=1):
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
    while not state.is_terminal():
        log("=======================================")
        log(pformat(state._tiles_by_player[state._current_player]))
        state = play_with_algo(
            players[state._current_player],
            state,
            game,
            num_samples,
            num_simulations=num_simulations,
            total_simulation_seconds=total_simulation_seconds
        )
        game.append(state)
        print_state(state)
    log(f"winneeeer {state.calc_reward()}")
    log(pformat(state._tiles_by_player))
    record_winner(state._tiles_by_player)

    return (game, state.calc_reward())

def record_winner(tiles_by_player):
    winners.append(tiles_by_player)


@click.command()
@click.option('-s','--simulations','num_simulations', default=None, help='number of simulations for MCTS', type=int)
@click.option('-b','--time-budget','total_simulation_seconds', default=1, help='Time budget for simulations in seconds', type=float)
@click.option('-m','--samples','num_samples', default=100, help='number of samples for PIMC')
@click.option('-t','--teams', nargs=2, default=('pimc', 'greedy') , help='Define algorithms by teams')
@click.option('-p','--players', nargs=4 , help='Define algorithms by players')
@click.option('-d','--debug','debug_flag', is_flag=True , help='Enables debug output')
@click.option('-w','--write', is_flag=True, help='Write games to file in ./simulations')
@click.option('-f','--file','file_path', help='Write games to file_path')
@click.argument('num_games', type=int)
def run(num_simulations, total_simulation_seconds, num_samples, teams, players, debug_flag, write, file_path, num_games):
    global debug
    global winners
    winners = []
    # random.seed(30)
    debug = debug_flag 
    game_results = []
    games = []
    if not players:
        players = create_players(teams)

    for i in range(num_games):
        print(f'\r... game {i}', end='', flush=True)
        game, winner = play_game(players, num_samples, num_simulations=num_simulations, total_simulation_seconds=total_simulation_seconds)
        game_results.append(winner)
        games.append(game)

    config = {
            'players':players,
            'num_simulations':num_simulations,
            'num_samples':num_samples,
            'num_games':num_games
    }
    print(' ')
    print(config)
    print(f"Porcentaje ganado {sum([result for result in game_results if result == 1])/len(game_results)}")
    if write or file_path:
        save_games_played(config, games, file_path)


def create_players(teams):
    return (teams[0], teams[1], teams[0], teams[1])

if __name__ == "__main__":
    run()





    
