from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from domino_state import DominoState, DominoAction

class DominoGameState(TwoPlayersGameMonteCarloTreeSearchNode):

    def __init__(self, state, next_to_move=0):
        self._state = DominoState(next_to_move, initial_state=state)

    @property
    def game_result(self):
        return self._state.calc_reward()

    def is_game_over(self):
        return self._state.is_terminal()

    def move(self, move):
        pass