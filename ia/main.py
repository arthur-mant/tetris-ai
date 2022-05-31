#import run_agent
import sys

sys.path.insert(0, '/home/martinelli/tetris-ia/tetris')

import tetris
import utils


if __name__ == '__main__':

    game = tetris.Tetris(20, 10)
    print(utils.get_state(game))
