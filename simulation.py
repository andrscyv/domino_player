from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
from domino_mctspy import DominoGameState
from domino_state import deal_tiles, DominoState, DominoAction
import random
from pprint import pformat
from pimc import pimc_decision
from recorder import Recorder
from simulation_utils import *
import click


def play_mcts(state, num_simulations=None, total_simulation_seconds=1):
    current_player = state._current_player
    tiles_by_player = state._tiles_by_player
    aux_state = DominoState(
        0,
        {
            "tiles_by_player": rotate(tiles_by_player, current_player),
            "suits_at_ends": state._suits_at_ends,
        },
    )
    root = TwoPlayersGameMonteCarloTreeSearchNode(state=DominoGameState(aux_state))
    mcts = MonteCarloTreeSearch(root)
    best_action = mcts.best_action(
        simulations_number=num_simulations,
        total_simulation_seconds=total_simulation_seconds,
    ).state._state.action
    return state.next_state_from_action(
        DominoAction(current_player, best_action.tile, best_action.suit_played)
    )


def play_greedy(state):
    actions = state.get_possible_actions()

    if len(actions) == 1:
        return state.next_state_from_action(actions[0])

    pips_of_actions = [sum(action.tile) for action in actions]
    index_of_greedy_action = pips_of_actions.index(max(pips_of_actions))

    return state.next_state_from_action(actions[index_of_greedy_action])


def build_pimc_params(state, game):
    played_tiles = {frozenset(s.action.tile) for s in game[1:]}
    my_tiles = {
        frozenset(tile) for tile in state._tiles_by_player[state._current_player]
    }
    num_tiles_by_player = [
        len(tiles) for tiles in rotate(state._tiles_by_player, state._current_player)
    ]

    return (state._suits_at_ends, my_tiles, played_tiles, num_tiles_by_player)


def play_pimc_with_preprocessing(
    state, game, num_samples, num_simulations=None, total_simulation_seconds=1
):
    possible_actions = state.get_possible_actions()

    if len(possible_actions) == 1:
        return state.next_state_from_action(possible_actions[0])

    return play_pimc(
        state, game, num_samples, num_simulations, total_simulation_seconds
    )


def play_pimc(
    state, game, num_samples, num_simulations=None, total_simulation_seconds=1
):
    suits_at_ends, my_tiles, played_tiles, num_tiles_by_player = build_pimc_params(
        state, game
    )

    tile, suit_played = pimc_decision(
        suits_at_ends,
        my_tiles,
        played_tiles,
        num_tiles_by_player,
        num_samples,
        mcts_simulations=num_simulations,
        total_simulation_seconds=total_simulation_seconds,
    )

    return state.next_state_from_action(
        DominoAction(state._current_player, tile, suit_played)
    )


def print_state(state):
    if not state.action:
        return

    log(
        f"\nPlayer: {state.action.player} {state.action.tile} suits: {state._suits_at_ends}"
    )


def log(message):
    if debug:
        print(message)


def play_turn(
    state,
    game,
    algo,
    total_simulation_seconds,
    num_samples,
):
    if algo == "mcts":
        return play_mcts(
            state,
            num_simulations=None,
            total_simulation_seconds=total_simulation_seconds,
        )

    if algo == "greedy":
        return play_greedy(state)

    if algo == "pimc":
        return play_pimc_with_preprocessing(
            state,
            game,
            num_samples,
            num_simulations=None,
            total_simulation_seconds=total_simulation_seconds,
        )


def play_game(players, recorder: Recorder):
    tiles_by_player = deal_tiles()
    first_player = random.choice([0, 1, 2, 3])
    state = DominoState(
        first_player, {"tiles_by_player": tiles_by_player, "suits_at_ends": set()}
    )
    game = [state]
    play_record_list = []
    log(f"Starts player {first_player}")
    log("Tiles : ")
    log(pformat(state._tiles_by_player))
    game_id = recorder.create_new_game_record(players, first_player, tiles_by_player)
    while not state.is_terminal():
        log("=======================================")
        log(pformat(state._tiles_by_player[state._current_player]))
        player_string = players[state._current_player]
        player_number = state._current_player
        algo, total_simulation_seconds, num_samples = parse_player_string(player_string)
        state = play_turn(state, game, algo, total_simulation_seconds, num_samples)
        game.append(state)
        play_record_list.append(
            PlayRecord(
                algo,
                total_simulation_seconds,
                num_samples,
                state,
                player_string,
                player_number,
            )
        )
        print_state(state)
    log(f"winneeeer {state.calc_reward()}")
    log(pformat(state._tiles_by_player))
    record_winner(state._tiles_by_player)
    recorder.save_record_list(game_id, play_record_list)
    winner = state.calc_reward()
    recorder.save_winner(game_id, winner)

    return (game, winner, play_record_list)


def record_winner(tiles_by_player):
    winners.append(tiles_by_player)


@click.command()
@click.option(
    "-t",
    "--teams",
    nargs=2,
    default=("pimc", "greedy"),
    help="Define algorithms by teams",
)
@click.option("-p", "--players", nargs=4, help="Define algorithms by players")
@click.option("-d", "--debug", "debug_flag", is_flag=True, help="Enables debug output")
@click.argument("num_games", type=int)
def run(
    teams,
    players,
    debug_flag,
    num_games,
):
    global debug
    global winners
    winners = []
    # random.seed(30)
    debug = debug_flag
    game_results = []
    game_record_list = []
    if not players:
        players = create_players(teams)

    recorder = Recorder("domino.db", num_games=num_games)
    for i in range(num_games):
        print(f"\r... game {i}", end="", flush=True)
        _, winner, play_record_list = play_game(players, recorder)
        game_results.append(winner)
        game_record_list.append(play_record_list)

    print(
        f"Porcentaje ganado {sum([result for result in game_results if result == 1])/len(game_results)}"
    )
    recorder.close()


def create_players(teams):
    return (teams[0], teams[1], teams[0], teams[1])


if __name__ == "__main__":
    run()
