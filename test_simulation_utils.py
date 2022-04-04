import unittest
from simulation_utils import parse_player_string


class TestSimulationUtils(unittest.TestCase):
    def test_parse_player_string_mcts(self):
        player_string = "mcts_0.00001"
        opts = parse_player_string(player_string)
        algo, total_simulation_seconds, num_samples = opts
        print(opts)
        self.assertEqual(algo, "mcts")
        self.assertEqual(total_simulation_seconds, 0.00001)

    def test_parse_player_string_pimc(self):
        player_string = "pimc_1_100"
        opts = parse_player_string(player_string)
        print(opts)
        algo, total_simulation_seconds, num_samples = opts
        self.assertEqual(algo, "pimc")
        self.assertEqual(total_simulation_seconds, 1)
        self.assertEqual(num_samples, 100)

    def test_parse_player_string_greedy(self):
        player_string = "greedy"
        opts = parse_player_string(player_string)
        print(opts)
        algo, total_simulation_seconds, num_samples = opts
        self.assertEqual(algo, "greedy")
        self.assertEqual(total_simulation_seconds, None)
        self.assertEqual(num_samples, None)

    def test_parse_player_string_pimc_missing_params(self):
        player_string = "pimc"
        self.assertRaises(ValueError, parse_player_string, player_string)

    def test_parse_player_string_pimc_missing_one_param(self):
        player_string = "pimc_0.10"
        self.assertRaises(ValueError, parse_player_string, player_string)

    def test_parse_player_string_pimc_param_wrong_type(self):
        player_string = "pimc_1_0.1"
        self.assertRaises(ValueError, parse_player_string, player_string)

    def test_parse_player_string_mcts_missing_param(self):
        player_string = "mcts"
        self.assertRaises(ValueError, parse_player_string, player_string)
