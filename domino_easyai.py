from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax
from domino_state import DominoState

class GameOfDomino( TwoPlayersGame ):

    def __init__(self, players):
        self.players = players
        self.nplayer = 1 # player 1 starts
        self._state = DominoState()

    def possible_moves(self): 
        return self._state.get_possible_actions() 

    def make_move(self,move): 
        # self.pile -= int(move) # remove bones.
        self._state = self._state.next_state_from_action(move)

    def win(self):
        #  return self.pile<=0 # opponent took the last bone ?
        winner = self._state.calc_reward()
        team_1 = self._state.team_1
        team_2 = self._state.team_2

        if winner == 0:
            return False

        if winner == team_1 and self.nplayer == 1:
            return True
        
        if winner == team_2 and self.nplayer == 2:
            return True

        return False
        

    def is_over(self): 
        # return self.win() # Game stops when someone wins.
        return self._state.is_terminal()

    def show(self): 
        # print ("%d bones left in the pile" % self.pile)
        print(self._state)

    def scoring(self): 
        return 100 if self.win() else 0 # For the AI

if __name__ == "__main__":
    # Start a match (and store the history of moves when it ends)
    ai = Negamax(32) # The AI will think 13 moves in advance
    game = GameOfDomino( [ Human_Player(), AI_Player(ai) ] )
    history = game.play()