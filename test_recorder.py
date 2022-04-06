import random
import unittest
from domino_state import DominoAction, DominoState, deal_tiles
from recorder import Recorder
from simulation_utils import PlayRecord


class TestRecorder(unittest.TestCase):
    def setUp(self):
        self.recorder = Recorder("domino_test.db")

    def test_record_creation(self):
        tiles_by_player = deal_tiles()
        simulation_id = self.recorder.create_new_simulation_record(
            ["mcts", "greedy", "pimc_1_100", "mcts"], "mcts", tiles_by_player
        )
        self.assertTrue(simulation_id > 0)
        first_player = random.choice([0, 1, 2, 3])
        initial_state = DominoState(
            first_player, {"tiles_by_player": tiles_by_player, "suits_at_ends": set()}
        )
        second_state = initial_state.next_state_from_action(
            DominoAction(0, tiles_by_player[0][0], None)
        )
        record_list = [
            PlayRecord(None, None, None, initial_state, None),
            PlayRecord("pimc", 1.1, 100, second_state, "pimc_1.1_100"),
        ]
        self.recorder.save_record_list(simulation_id, record_list)
