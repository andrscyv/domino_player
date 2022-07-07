# Partners Dominoes PIMC player

This is an ai player for the game of partnership [dominoes](https://en.wikipedia.org/wiki/Dominoes) (2 opposing teams of 2 players each).

Given the current state of the game's public information (played tiles excluding other player's hidden tiles) the ai will generate a set of possible scenarios of perfect information by uniformly sampling from the possible configurations of the hidden tiles. In each scenario the ai will run [MCTS](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search) to generate a move. The ai will then select the move with the most wins.

## Cli (WIP)

Define a domino game in json format and the cli returns the selected tile to be played by current player

## Simulations

The simulations cli runs a number of games with the team
configuration provided. On the experiments/ folder there are shell scripts with some examples.
