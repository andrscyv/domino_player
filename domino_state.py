import random

def deal_tiles():
    tiles = [ {i,k} for i in range(7) for k in range(i,7)]
    tiles_by_player = []
    random.shuffle(tiles)

    for i in range(4):
        tiles_by_player.append(tiles[i*7:(i*7)+7])

    return tiles_by_player

class DominoAction:
    def __init__(self, player, tiles):
        self.player = player
        self.tiles = tiles

class DominoState:

    def __init__(self, current_player = 0, initial_state = None):

        self._current_player = current_player

        if initial_state is None:
            self._tiles_by_player = deal_tiles()
            self._suits_at_ends = {} 
        else:
            self._tiles_by_player = initial_state['tiles_by_player']
            self._suits_at_ends = initial_state['suits_at_ends']

    def get_possible_actions(self):
        if not self._suits_at_ends:
            possible_actions =  self._tiles_by_player[self._current_player][:]
        else:
            possible_actions =  [ tile for tile in self._tiles_by_player[self._current_player] if self._suits_at_ends.intersection(tile)]

            if len(possible_actions) == 0:
                possible_actions = [{-1}]
            
        return DominoAction(self._current_player, possible_actions)