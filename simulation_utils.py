from collections import namedtuple

PlayRecord = namedtuple(
    "GameRecord", ["algo", "time_budget", "num_samples", "state", "player_string"]
)


def parse_player_string(player_string):
    algo = None
    total_simulation_seconds = None
    num_samples = None
    params = player_string.split("_")

    if params[0] == "pimc":  # pimc needs two parameters
        if len(params) < 3:
            raise ValueError("Missing params for pimc: {}".format(player_string))

        algo, total_simulation_seconds, num_samples = params

    elif params[0] == "greedy":
        algo = params[0]

    elif params[0] == "mcts":
        if len(params) < 2:
            raise ValueError("Missing params for mcts: {}".format(player_string))
        algo, total_simulation_seconds = params

    total_simulation_seconds = (
        float(total_simulation_seconds) if total_simulation_seconds else None
    )
    num_samples = int(num_samples) if num_samples else None

    return algo, total_simulation_seconds, num_samples


def rotate(l, n):
    return l[n:] + l[:n]
