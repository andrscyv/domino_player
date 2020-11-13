import random
from mctspy.games.common import  AbstractGameAction

def deal_tiles():
    tiles = [ {i,k} for i in range(7) for k in range(i,7)]
    tiles_by_player = []
    random.shuffle(tiles)

    for i in range(4):
        tiles_by_player.append(tiles[i*7:(i*7)+7])

    return tiles_by_player

def sum_points(tiles):
    points = 0

    for tile in tiles:
        if len(tile) > 1:
            points += sum(tile)
        else:
            assert(len(tile) == 1)
            points += 2* sum(tile)

    return points

class DominoAction(AbstractGameAction):
    def __init__(self, player, tile):
        self.player = player
        self.tile = tile

    def __repr__(self):
        return f"player:{self.player} tile: {self.tile}"

class DominoState:
    team_1 = 1
    team_2 = -1

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
        try:
            tiles[action.player].remove(action.tile)
        except ValueError:
            pass
        suits_at_ends = self._suits_at_ends
        
        return DominoState((action.player + 1) % 4, {
            'tiles_by_player':tiles,
            'suits_at_ends': suits_at_ends if len(action.tile) == 1 else suits_at_ends.symmetric_difference(action.tile)
        })
    
    def calc_reward(self):
        num_tiles_by_player = [ len(tiles) for tiles in self._tiles_by_player ]

        if 0 in num_tiles_by_player:
            if num_tiles_by_player.index(0) % 2 == 0:
                reward = self.team_1
            else:
                reward = self.team_2
        else:
            if self._game_is_closed():
                reward = self._team_with_fewer_points()
            else:
                reward = 0

        return reward

    def is_terminal(self):
        num_tiles_by_player = [ len(tiles) for tiles in self._tiles_by_player ]
        return (0 in num_tiles_by_player) or self._game_is_closed()


    def _game_is_closed(self):

        for tiles in self._tiles_by_player:
            for tile in tiles:
                if tile & self._suits_at_ends:
                    return False

        return True

    def _team_with_fewer_points(self):
        points_team_1 = sum_points(self._tiles_by_player[0] + self._tiles_by_player[2])
        points_team_2 = sum_points(self._tiles_by_player[1] + self._tiles_by_player[3])

        if points_team_1 ==  points_team_2:
            return 0
        else:
            if points_team_1 < points_team_2:
                return self.team_1
            else:
                return self.team_2

    def _is_action_legal(self,action):
        is_performed_by_current_player = action.player == self._current_player
        tile_belongs_to_current_player = action.tile in self._tiles_by_player[self._current_player]
        tile_is_playable = bool(action.tile & self._suits_at_ends)

        return is_performed_by_current_player and tile_belongs_to_current_player and tile_is_playable

