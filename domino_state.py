import random

def deal_tiles():
    tiles = [ {i,k} for i in range(7) for k in range(i,7)]
    tiles_by_player = []
    random.shuffle(tiles)

    for i in range(4):
        tiles_by_player.append(tiles[i*7:(i*7)+7])

    return tiles_by_player

class DominoAction:
    def __init__(self, player, tile):
        self.player = player
        self.tile = tile

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
            possible_tiles =  self._tiles_by_player[self._current_player][:]
        else:
            possible_tiles =  [ tile for tile in self._tiles_by_player[self._current_player] if self._suits_at_ends.intersection(tile)]

            if len(possible_tiles) == 0:
                possible_tiles = [{-1}]
            
        return [ DominoAction(self._current_player, tile) for tile in possible_tiles] 

    def next_state_from_action(self, action):
        tiles = [ tiles[:] for tiles in self._tiles_by_player ]
        tiles[action.player].remove(action.tile)
        suits_at_ends = self._suits_at_ends
        
        return DominoState((action.player + 1) % 4, {
            'tiles_by_player':tiles,
            'suits_at_ends': suits_at_ends if len(action.tile) == 1 else suits_at_ends.symmetric_difference(action.tile)
        })