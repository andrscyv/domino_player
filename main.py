from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
from domino import DominoGameState
from domino_state import deal_tiles, DominoState
import numpy

# def play(board, time):
#     state = board
#     initial_board_state = TicTacToeGameState(state = state, next_to_move=-1)

#     root = TwoPlayersGameMonteCarloTreeSearchNode(state = initial_board_state)
#     mcts = MonteCarloTreeSearch(root)
#     return mcts.best_action(time).state.board

# def play_move(x,y, player):
#     global board

#     board[x,y] = player
#     print(board)
#     winner = evaluate(board)
#     if winner != 0:
#         print('Winner: ', winner)
#         board = create_board()
#         print(board)


# def uct():
#     move = uct_decision(TicTacToeState(board=board), num_iterations=8000)
#     play_move(move[0], move[1], 1)

# def play(x,y):
#     play_move(x,y,2)
#     uct()

# def new():
#     global board
#     board = create_board()
#     print(board)

if __name__ == "__main__":
    global game , current_player
    current_player = 0
    state = DominoState(0, {
        'tiles_by_player': deal_tiles(),
        'suits_at_ends': set()
    })
    game = DominoGameState(state)
    root = TwoPlayersGameMonteCarloTreeSearchNode(state = game)
    mcts = MonteCarloTreeSearch(root)
    action = mcts.best_action(1)
    print(action)