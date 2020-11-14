from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
from domino import DominoGameState
from domino_state import deal_tiles, DominoState
import numpy
import pprint

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
    # tiles_by_player = deal_tiles()
    # suits_at_ends = set()
    # tiles_by_player = [[{0, 1}, {4}, {0, 5}, {0, 4}, {1, 5}, {0, 2}, {3, 6}],
    #                    [{1, 3}, {5, 6}, {2}, {3}, {0}, {4, 6}, {2, 5}],
    #                    [{2, 3}, {6}, {4, 5}, {3, 5}, {2, 6}, {5}, {1, 6}],
    #                    [{0, 3}, {1}, {2, 4}, {0, 6}, {1, 4}, {3, 4}, {1, 2}]]
    tiles_by_player = [[{0, 1}, {4},],
                       [{1, 3}, {5, 6},],
                       [{2, 3}, {6}, ],
                       [{0, 3}, {1} ]]
    suits_at_ends =  {2,4}
    state = DominoState(current_player, {
        'tiles_by_player': tiles_by_player,
        'suits_at_ends': suits_at_ends
    })
    game = DominoGameState(state)
    root = TwoPlayersGameMonteCarloTreeSearchNode(state = game)
    mcts = MonteCarloTreeSearch(root)
    action = mcts.best_action(1000)
    pp = pprint.PrettyPrinter()
    pp.pprint(state._tiles_by_player)
    print(action.state._state.action)