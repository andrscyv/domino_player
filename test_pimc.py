import unittest
from pimc import sample_combinations, pimc_decision, sample_hands_uniformly
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

    def test_sample_hands_uniformly(self):
        played_tiles = {frozenset({5,2}),frozenset({2}),frozenset({2,3}),frozenset({3})}
        my_tiles = {frozenset({1}), frozenset({2,4}), frozenset({4}), frozenset({6,1}), frozenset({2,6}), frozenset({0,2})}
        num_tiles_by_player = [6,6,6,6]
        sample_size = 30 

        first_hand_sample, second_hand_sample, third_hand_sample = sample_hands_uniformly(played_tiles, my_tiles, num_tiles_by_player, sample_size)

        for i in range(sample_size):
            self.assertFalse(first_hand_sample[i]&second_hand_sample[i])
            self.assertFalse(first_hand_sample[i]&third_hand_sample[i])
            self.assertFalse(first_hand_sample[i]&my_tiles)
            self.assertFalse(second_hand_sample[i]&third_hand_sample[i])
            self.assertFalse(second_hand_sample[i]&my_tiles)
            self.assertFalse(third_hand_sample[i]&my_tiles)


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
            { frozenset(tile) for tile in tiles_by_player[0]}, 
            played_tiles, 
            [len(tiles) for tiles in tiles_by_player])
