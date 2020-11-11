import unittest
from dominoes_state import DominoesState, deal_tiles

class TestDominoesState(unittest.TestCase):

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
        state = DominoesState( 1,{
            'tiles_by_player':[
                [{0}, {1, 2}, {1, 5}, {6}, {5, 6}, {4, 6}], 
                [{5}, {2, 5}, {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
                [{4}, {3}, {4, 5}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
                [{3, 4}, {0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
                ],
            'suits_at_ends':{2,3}
        })

        self.assertEqual(state.get_possible_actions(), [{2,5}, {1,3}, {2,4}, {2}, {3,5}])
         
    def test_get_possible_moves_returns_pass_action(self):
        state = DominoesState( 1,{
            'tiles_by_player':[
                [{0}, {1, 2}, {1, 5}, {5, 6}, {4, 6}, {2,3}], 
                [{5}, {2, 5}, {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
                [{4}, {3}, {4, 5}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
                [{3, 4}, {0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
                ],
            'suits_at_ends':{6}
        })

        self.assertEqual(state.get_possible_actions(), [{-1}])

    def test_get_possible_moves_returns_all_tiles(self):
        state = DominoesState( 1,{
            'tiles_by_player':[
                [{0}, {1, 2}, {1, 5}, {5, 6},{6},{4, 6}, {2,3}], 
                [{5}, {2, 5}, {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
                [{4}, {3}, {4, 5}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
                [{3, 4}, {0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
                ],
            'suits_at_ends': set()
        })

        self.assertEqual(state.get_possible_actions(), [{5}, {2, 5}, {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}])