from domino_state import DominoState
import unittest
from pimc import mcts_decision

class TestMcts(unittest.TestCase):

    def test_player_pass_if_no_tiles_to_play(self):
        state = DominoState(0, {
            'tiles_by_player':[
                [{2}],
                [{0, 2}, {2, 3}, {4}],
                [{0,6}],
                [{0}]
            ],
            'suits_at_ends':{3,6}
        })
        print(mcts_decision(state).action)