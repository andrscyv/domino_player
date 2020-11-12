import unittest
from domino_state import DominoState, deal_tiles

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
        self.assertEqual(actions.tiles, [{2,5}, {1,3}, {2,4}, {2}, {3,5}])
        self.assertEqual(actions.player, 1)
         
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
        self.assertEqual(actions.tiles, [{-1}])
        self.assertEqual(actions.player, 1)

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
        self.assertEqual(actions.tiles, [{5}, {2, 5}, {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}])
        self.assertEqual(actions.player, 1)