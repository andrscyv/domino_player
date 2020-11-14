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

def calculate_suits_at_ends(previous_suits, tile_played, suit_played):

    if tile_played == {-1}: # {-1} represents that player pass
        return previous_suits

    if previous_suits == {}: #at begining of game
        return tile_played

    if len(tile_played) == 1 : #double doesnt change suits
        return previous_suits

    if len(previous_suits) == 1:
        return tile_played 

    assert( suit_played in previous_suits & tile_played )
    assert(len(tile_played) == 2 ) 
    assert(len(previous_suits)==2)
    return (previous_suits | tile_played) - {suit_played}

class DominoAction(AbstractGameAction):
    def __init__(self, player, tile, suit_played):
        self.player = player
        self.tile = tile
        self.suit_played = suit_played

    def __repr__(self):
        return f"player:{self.player} tile: {self.tile}"

class DominoState:
    team_1 = 1
    team_2 = -1

    def __init__(self, current_player = 0, initial_state = None, action = None):

        self._current_player = current_player

        if initial_state is None:
            self._tiles_by_player = deal_tiles()
            self._suits_at_ends = {} 
        else:
            self._tiles_by_player = initial_state['tiles_by_player']
            self._suits_at_ends = initial_state['suits_at_ends']

        if action:
            self.action = action

    def get_possible_actions(self):
        player_tiles = self._tiles_by_player[self._current_player]

        if not self._suits_at_ends:
            return [ DominoAction(self._current_player, tile, None) for tile in player_tiles]

        possible_actions=[]
        for tile in player_tiles:
            for suit in tile & self._suits_at_ends:
                possible_actions.append(DominoAction(self._current_player, tile, suit))

        if len(possible_actions) == 0:
            return [DominoAction(self._current_player, {-1}, None)]

        return possible_actions

    def next_state_from_action(self, action):
        tiles = [ tiles[:] for tiles in self._tiles_by_player ]

        if action.tile != {-1}:
            tiles[action.player].remove(action.tile)
        
        return DominoState((action.player + 1) % 4, {
            'tiles_by_player':tiles,
            'suits_at_ends': calculate_suits_at_ends(self._suits_at_ends, action.tile, action.suit_played) 
        }, action = action)
    
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
        if not self._suits_at_ends:
            return False

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
        tile_is_playable = bool(action.tile & self._suits_at_ends) or (not self._suits_at_ends)
        action_is_to_pass = action.tile == {-1}

        return is_performed_by_current_player and ((tile_belongs_to_current_player and tile_is_playable) or action_is_to_pass)

    def current_team(self):
        return self.team_1 if self._current_player % 2 == 0 else self.team_2

    def __repr__(self):
        return f" <Player:{self._current_player} suits_at_ends: {self._suits_at_ends}>"

