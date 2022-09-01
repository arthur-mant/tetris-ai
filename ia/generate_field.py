import sys
sys.path.insert(0, '/home/martinelli/tetris-ia/tetris')
from tetris import Piece
import numpy as np
import utils
import random
import copy
import time

def generate_experience_db(width, height, num):

    input_v = []
    action_v = []
    piece_v = []
    next_piece_v = []

    begin_time = time.time()
    #aux_time = time.time()

    for i in range(num):
        aux = generate_plain_field(
            width, height,
            random.randint(4, height-2),
            random.gauss(1.5, 0.5)
        )
        if aux != None:
            inp, action, piece, next_piece = aux
            aux_arr = [ 0 for i in range(40) ]
            aux_arr[action] = 1
            input_v.append(inp)
            action_v.append(aux_arr)
            piece_v.append(piece)
            next_piece_v.append(next_piece)


        #if i % 1000 == 0:
        #    print("time for ", i//1000, "th batch of 1000: ", time.time()-aux_time, "s")
        #    aux_time = time.time()

    print("Took ", time.time()-begin_time, "s to generate exp db of ", num, " entries")

    return input_v, action_v, piece_v, next_piece_v

def generate_plain_field(width, height, pile_height, bump_factor):

    if (width <= 5):
        print("ERROR: board too narrow")
        return None
    if (height <= 5):
        print("ERROR: board too small")
        return None
    if (pile_height >= height) or (pile_height < 0):
        print("ERROR: invalid board pile_height: ", pile_height)
        return None
    if (bump_factor <= 0):
        #print("ERROR: invalid bump_factor: ", bump_factor)
        #return None
        bump_factor = 0.1


    field = generate_empty_field(width, height)

    for i in range(pile_height, height):            #cria bloco
        for j in range(len(field[pile_height])):
            field[i][j] = 1

    for i in range(pile_height+1, height):          #cria buracos
        holes = int(random.gauss(2.5, 1))
        holes = max(1, holes)
        holes = min(width//2, holes)

        for j in range(holes):
            field[i][random.randint(0, width-1)] = 0

    piece = random.randint(0, len(Piece.pieces)-1)
    next_piece = random.randint(0, len(Piece.pieces)-1)
    action = random.randint(0, 4*width-1)

    pos, rot = utils.translate_action(action, piece, Piece.pieces)

    possible_y = []

    for y in range(-1, height):
        top_most_layer = 4*[10]
        overrode_border = False
        collided = False
        for block in Piece.pieces[piece][rot]:
            l = block // 4
            c = block % 4

            if  pos+c < 0 or pos+c >= width:
                overrode_border = True
                break

            if y+l >= height or field[y+l][pos+c] == 1:
                collided = True

            top_most_layer[c] = min(top_most_layer[c], l)

        if overrode_border:
            print("board overriden, pos = ", pos)
            break

        lowest_top_layer = 0
        for layer in top_most_layer:
            if layer < 4:
                lowest_top_layer = max(lowest_top_layer, layer)


        if y+lowest_top_layer <= pile_height and collided:
            possible_y.append(y)

    if len(possible_y) == 0:
        return None

    chosen_y = random.sample(possible_y, 1)[0]
    columns_used = 4*[0]

    for block in Piece.pieces[piece][rot]:
        l = block // 4
        c = block % 4

        field[chosen_y+l][pos+c] = 0
        columns_used[c] = 1

    used_columns = []
    for i in range(len(columns_used)):
        if columns_used[i] == 1:
            used_columns.append(pos+i)

    return field, action, piece, next_piece



def generate_empty_field(width, height):
    field = [ [ 0 for i in range(width) ] for j in range(height) ]
    return field


if __name__ == '__main__':
    state, action, piece, next_piece = generate_experience_db(10, 20, 1)

    if len(state) == 0:
        print("failed to generate field, try again")
        exit(0)

    utils.display_field(state[0], np.argmax(action[0]), piece[0], Piece.pieces)
    print(action[0])
    print(np.argmax(action[0]))

    #aux = generate_experience_db(10, 20, 100000)
