import unittest
from pimc import sample_combinations, pimc_decision
from domino_state import build_tiles, deal_tiles



class TestPimc(unittest.TestCase):

    def test_sample_combinations(self):
        tiles = build_tiles()
        sample_size = 100
        sample = sample_combinations(tiles, 7, sample_size)
        self.assertEquals(len(sample), sample_size)
        for hand in sample :
            self.assertEqual(len(hand), 7)
            self.assertEquals(len(hand & tiles), len(hand))

    def test_pimc_desicion(self):
        tiles_by_player = [
            [{0}, {1, 2}, {1, 5}, {6}, {5, 6}, {4, 6}], 
            [{5},  {0, 5}, {1, 3}, {2, 4}, {2}, {3, 5}], 
            [{4}, {3}, {0, 1}, {0, 6}, {1, 6}, {0, 2}], 
            [{0, 3}, {2, 6}, {1, 4}, {0, 4}, {3, 6}, {1}]
        ] 
        played_tiles = {frozenset({4,5}), frozenset({5,2}), frozenset({2,3}), frozenset({3,4})}
        pimc_decision(
            {4},
            tiles_by_player[0], 
            played_tiles, 
            [len(tiles) for tiles in tiles_by_player])
