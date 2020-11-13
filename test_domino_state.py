import unittest
from domino_state import DominoState, DominoAction, deal_tiles, sum_points
import copy

class TestDominoState(unittest.TestCase):

    def test_create_random_player_tiles(self):
        tiles_by_player = deal_tiles()
        self.assertEqual(len(tiles_by_player), 4)

        for player_tiles in tiles_by_player:
            self.assertEqual(len(player_tiles),7)

        tiles = [ tile for player_tiles in tiles_by_player for tile in player_tiles ]
        possible_tiles = [ {i,k} for i in range(7) for k in range(i,7)]

        for tile in possible_tiles:
            self.assertIn(tile, tiles)
        

    def test_get_possible_moves(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{0}, {1, 2}, {1, 5}, {6}, {5, 6}, {4, 6}], 
                [{5}, {2, 5}, {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
                [{4}, {3}, {4, 5}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
                [{3, 4}, {0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
                ],
            'suits_at_ends':{2,3}
        })
        actions = state.get_possible_actions()
        for action in actions:
            self.assertIn(action.tile, [{2,5}, {1,3}, {2,4}, {2}, {3,5}])
            self.assertEqual(action.player, 1)
         
    def test_get_possible_moves_returns_pass_action(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{0}, {1, 2}, {1, 5}, {5, 6}, {4, 6}, {2,3}], 
                [{5}, {2, 5}, {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
                [{4}, {3}, {4, 5}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
                [{3, 4}, {0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
                ],
            'suits_at_ends':{6}
        })

        actions = state.get_possible_actions()
        for action in actions:
            self.assertIn(action.tile, [{-1}])
            self.assertEqual(action.player, 1)

    def test_get_possible_moves_returns_all_tiles(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{0}, {1, 2}, {1, 5}, {5, 6},{6},{4, 6}, {2,3}], 
                [{5}, {2, 5}, {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
                [{4}, {3}, {4, 5}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
                [{3, 4}, {0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
                ],
            'suits_at_ends': set()
        })

        actions = state.get_possible_actions()
        for action in actions:
            self.assertIn(action.tile, [{5}, {2, 5}, {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}])
            self.assertEqual(action.player, 1)
        
    def test_next_state_from_action(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{0}, {1, 2}, {1, 5}, {6}, {5, 6}, {4, 6}], 
                [{5}, {2, 5}, {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
                [{4}, {3}, {4, 5}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
                [{3, 4}, {0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
                ],
            'suits_at_ends':{2,3}
        })
        next_state = state.next_state_from_action(DominoAction(1, {2,5}))
        self.assertEqual(next_state._current_player, 2)
        self.assertEqual(next_state._suits_at_ends, {5,3})
        self.assertEqual(next_state._tiles_by_player, [
                [{0}, {1, 2}, {1, 5}, {6}, {5, 6}, {4, 6}], 
                [{5},{0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
                [{4}, {3}, {4, 5}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
                [{3, 4}, {0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
        ])

    def test_next_state_from_pass_action(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{0}, {1, 2}, {1, 5}, {6}, {5, 6}, {4, 6}], 
                [{5}, {2, 5}, {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
                [{4}, {3}, {4, 5}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
                [{3, 4}, {0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
                ],
            'suits_at_ends':{2,3}
        })
        next_state = state.next_state_from_action(DominoAction(1, {-1}))
        self.assertEqual(next_state._current_player, 2)
        self.assertEqual(next_state._suits_at_ends, {2,3})
        self.assertEqual(next_state._tiles_by_player, [
                [{0}, {1, 2}, {1, 5}, {6}, {5, 6}, {4, 6}], 
                [{5},{2,5},{0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
                [{4}, {3}, {4, 5}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
                [{3, 4}, {0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
        ])

    def test_next_state_from_single_value_tile_action(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{0}, {1, 2}, {1, 5}, {6}, {5, 6}, {4, 6}], 
                [{5}, {2, 5}, {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
                [{4}, {3}, {4, 5}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
                [{3, 4}, {0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
                ],
            'suits_at_ends':{2,3}
        })
        next_state = state.next_state_from_action(DominoAction(1, {2}))
        self.assertEqual(next_state._current_player, 2)
        self.assertEqual(next_state._suits_at_ends, {2,3})
        self.assertEqual(next_state._tiles_by_player, [
                [{0}, {1, 2}, {1, 5}, {6}, {5, 6}, {4, 6}], 
                [{5}, {2,5},{0, 5}, {1, 3}, {2, 4}, {3, 5}], 
                [{4}, {3}, {4, 5}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
                [{3, 4}, {0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
        ])

    def test_next_state_from_action_creates_deep_copy(self):
        tiles_by_player = [
                [{0}, {1, 2}, {1, 5}, {6}, {5, 6}, {4, 6}], 
                [{5}, {2, 5}, {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
                [{4}, {3}, {4, 5}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
                [{3, 4}, {0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
                ]
        state = DominoState( 1,{
            'tiles_by_player':copy.deepcopy(tiles_by_player),
            'suits_at_ends':{2,3}
        })
        next_state = state.next_state_from_action(DominoAction(1, {2,5}))
        next_state._tiles_by_player[0].remove({0})
        self.assertEqual(tiles_by_player, state._tiles_by_player)
        self.assertIn({0}, state._tiles_by_player[0])
        self.assertNotIn({0}, next_state._tiles_by_player[0])
        self.assertIn({2,5}, state._tiles_by_player[1])
        self.assertNotIn({2,5}, next_state._tiles_by_player[1])
    
    def test_game_is_closed(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{4, 6}, {5,3}], 
                [{3, 5}], 
                [{4} ], 
                [{4,1}]
                ],
            'suits_at_ends':{2}
        })

        self.assertTrue(state._game_is_closed())

    def test_game_is_not_closed(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{4, 6}, {5,3}], 
                [{3, 5}], 
                [{4} ], 
                [{4,1}]
                ],
            'suits_at_ends':{2,1}
        })

        self.assertFalse(state._game_is_closed())

    def test_sum_points_no_double(self):
        tiles = [{2,3}, {3,4},{4,2},{1,0}]
        self.assertEqual(19, sum_points(tiles))

    def test_sum_points_with_doubles(self):
        tiles = [{3}, {0,4},{4,2},{1},{2,0}]
        self.assertEqual(20, sum_points(tiles))

    def test_team1_has_fewer_points(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{4, 2}, {5,1}], 
                [{5}], 
                [{2} ], 
                [{4,6}]
                ],
            'suits_at_ends':{3}
        })

        self.assertEqual(state._team_with_fewer_points(), state.team_1)

    def test_team2_has_fewer_points(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{4, 6}, {5,1}], 
                [{3, 1}], 
                [{4} ], 
                [{4,3}]
                ],
            'suits_at_ends':{2}
        })

        self.assertEqual(state._team_with_fewer_points(), state.team_2)

    def test_teams_have_same_amount_of_points(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{4, 6}, {5,1}], 
                [{3, 1},{5} ], 
                [{4} ], 
                [{4,3}, {3,0}]
                ],
            'suits_at_ends':{2}
        })

        self.assertEqual(state._team_with_fewer_points(), 0)


    def test_calc_reward_team2_win(self):
        state = DominoState( 0,{
            'tiles_by_player':[
                [{4, 6}], 
                [{3, 5}], 
                [{4} ], 
                []
                ],
            'suits_at_ends':{4,3}
        })
        self.assertEqual(state.calc_reward(), -1)

    def test_calc_reward_team1_win(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [], 
                [{3, 5}], 
                [{4} ], 
                [{5}]
                ],
            'suits_at_ends':{4,3}
        })
        self.assertEqual(state.calc_reward(), 1)

    def test_calc_reward_team1_win_by_points(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{5,0}], 
                [{3, 5}], 
                [{0} ], 
                [{5}]
                ],
            'suits_at_ends':{2}
        })
        self.assertEqual(state.calc_reward(), 1)

    def test_calc_reward_team2_win_by_points(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{5,4}], 
                [{3, 5}], 
                [{6} ], 
                [{5}]
                ],
            'suits_at_ends':{2}
        })
        self.assertEqual(state.calc_reward(), -1)

    def test_is_terminal_team1_win(self):
        state = DominoState( 0,{
            'tiles_by_player':[
                [{5,4}], 
                [{3, 5}], 
                [{6} ], 
                []
                ],
            'suits_at_ends':{2}
        })
        self.assertTrue(state.is_terminal())

    def test_is_terminal_game_closed(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{5,4}], 
                [{3, 5}], 
                [{6} ], 
                [{1,0}]
                ],
            'suits_at_ends':{2}
        })
        self.assertTrue(state.is_terminal())
    
    def test_action_is_legal(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{0}, {1, 2}, {1, 5}, {5, 6}, {4, 6}, {6}], 
                [{5}, {2, 5}, {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
                [{4}, {3}, {4, 5}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
                [{3, 4}, {0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
                ],
            'suits_at_ends':{2,3}
        })
        action = DominoAction(1, {2,5})
        self.assertTrue(state._is_action_legal(action))

    def test_action_is_legal_tile_doesnt_belong_to_player(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{0}, {1, 2}, {1, 5}, {5, 6}, {4, 6}, {6}], 
                [{5}, {2, 5}, {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
                [{4}, {3}, {4, 5}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
                [{3, 4}, {0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
                ],
            'suits_at_ends':{2,3}
        })
        action = DominoAction(1, {1,2})
        self.assertFalse(state._is_action_legal(action))

    def test_action_is_ilegal_tile_isnt_playable(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{0}, {1, 2}, {1, 5}, {5, 6}, {4, 6}, {6}], 
                [{5}, {2, 5}, {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
                [{4}, {3}, {4, 5}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
                [{3, 4}, {0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
                ],
            'suits_at_ends':{2,3}
        })
        action = DominoAction(1, {5})
        self.assertFalse(state._is_action_legal(action))

    def test_action_is_ilegal_not_current_player(self):
        state = DominoState( 1,{
            'tiles_by_player':[
                [{0}, {1, 2}, {1, 5}, {5, 6}, {4, 6}, {6}], 
                [{5}, {2, 5}, {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
                [{4}, {3}, {4, 5}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
                [{3, 4}, {0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
                ],
            'suits_at_ends':{2,3}
        })
        action = DominoAction(0, {1,2})
        self.assertFalse(state._is_action_legal(action))
