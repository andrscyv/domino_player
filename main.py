import numpy as np
from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
from mctspy.games.examples.tictactoe import TicTacToeGameState

state = np.zeros((3,3))
initial_board_state = TicTacToeGameState(state = state, next_to_move=1)

root = TwoPlayersGameMonteCarloTreeSearchNode(state = initial_board_state)
mcts = MonteCarloTreeSearch(root)

def play(board, time):
    state = board
    initial_board_state = TicTacToeGameState(state = state, next_to_move=-1)

    root = TwoPlayersGameMonteCarloTreeSearchNode(state = initial_board_state)
    mcts = MonteCarloTreeSearch(root)
    return mcts.best_action(time).state.board

