from domino_state import DominoState, DominoAction
from mctspy.games.common import TwoPlayersAbstractGameState

class DominoGameState(TwoPlayersAbstractGameState):

    def __init__(self, state, next_to_move=1):
        self._state = state
        self.next_to_move = next_to_move

    @property
    def game_result(self):
        return self._state.calc_reward()

    def is_game_over(self):
        return self._state.is_terminal()

    def is_move_legal(self, move):
        return self._state._is_action_legal(move)

    def move(self, move):
        if not self.is_move_legal(move):
            raise ValueError(
                f"move {move} for state {self._state} is not legal"
            )

        next_state = self._state.next_state_from_action(move)
        return DominoGameState(next_state, next_to_move = next_state.current_team())
    
    def get_legal_actions(self):
        return self._state.get_possible_actions()