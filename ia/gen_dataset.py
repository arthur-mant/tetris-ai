import pickle
import numpy as np
import sys
sys.path.insert(0, './tetris')

from tetris import Piece
import generate_field
import utils

def gen_dataset(filename, num):

    input_shape = ([20, 10, 1], [(7-1)])
    action_size = 40

    state, piece, action = generate_field.generate_experience_db(10, 20, num, 1)

    X_v = []
    Y_v = []

    X_v = [np.reshape(state, [len(state)]+input_shape[0]),
            np.reshape(piece, [len(piece)]+input_shape[1])]
    Y_v = np.reshape(action, [len(state), action_size])

    data = {
        "X": X_v,
        "Y": Y_v
    }

    with open(filename, 'wb') as f:
        pickle.dump(data, f)

if __name__ == '__main__':
    gen_dataset("dataset.pickle", 10000)

    with open("dataset.pickle", 'rb') as f:
        data = pickle.load(f)
    state = data["X"][0][0]
    piece = data["X"][1][0]
    action = data["Y"][0]
    print("Example:")
    utils.display_field(state, np.argmax(action), utils.piece_num(piece), Piece.pieces)
