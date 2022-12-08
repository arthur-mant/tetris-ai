import sys
sys.path.insert(0, '/home/martinelli/tetris-ia/tetris')
from tetris import Piece
import numpy as np
import utils
import random
import copy
import time

def generate_experience_db(width, height, num, depth):

    input_v = []
    action_v = []
    piece_v = []

    num_pieces = 7

    begin_time = time.time()
    #aux_time = time.time()

    j = 0

    while len(input_v) < num and j < 2*num:
        aux = generate_plain_field(
            width, height,
            random.randint(4, height-2),
            random.gauss(1.5, 0.5),
            depth
        )
        if aux != None:
            for play in aux:
                table, action, piece = play
                aux_arr = [ 0 for i in range(40) ]
                aux_arr[action] = 12000
                action_v.append(aux_arr)

                aux_arr = [ 0 for i in range(7-1) ]
                for i in range(0, num_pieces-1):
                    if piece == i:
                        aux_arr[i] = 1
                piece_v.append(aux_arr)

                input_v.append(table)

        j += 1


        #if i % 1000 == 0:
        #    print("time for ", i//1000, "th batch of 1000: ", time.time()-aux_time, "s")
        #    aux_time = time.time()

    print("Took ", time.time()-begin_time, "s to generate experience data of ", len(input_v), " entries")
    print("tried ", j, " times")

    return input_v, piece_v, action_v

def generate_plain_field(width, height, pile_height, bump_factor, max_tables):

    max_height = 3

    if (width <= 5):
        print("ERROR: board too narrow")
        return None
    if (height <= 5):
        print("ERROR: board too small")
        return None
    if (pile_height >= height) or (pile_height < max_height):
        print("ERROR: invalid board pile_height: ", pile_height)
        return None
    if (bump_factor <= 0):
        #print("ERROR: invalid bump_factor: ", bump_factor)
        #return None
        bump_factor = 0.1


    field = generate_empty_field(width, height)
    field = cria_bloco(field, pile_height, height)

    play_v = []
    altered_columns = set()

    i = 0
    while len(play_v) < max_tables and i < 2*max_tables:
        aux = tira_peça(field, altered_columns, width, height)
        if aux != None:
            field = aux[0][0]
            play_v.append((aux[0][1], aux[0][2]))
            altered_columns.update(aux[1])
        i += 1

    if len(play_v) == 0:
        return None

    deepest_hole = 0

    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] == 0:
                deepest_hole = max(deepest_hole, i)


    field = torna_irregular(field, pile_height, list(altered_columns), max_height, height)
    field = esburaca(field, deepest_hole, width, height)


    out_v = [ None for i in range(len(play_v)) ]

    out_v[-1] = (field, play_v[-1][0], play_v[-1][1])

    for i in range(len(play_v)-1-1, -1, -1):
        out_v[i] = (coloca_peca(copy.deepcopy(out_v[i+1][0]), play_v[i+1][0], play_v[i+1][1]), play_v[i][0], play_v[i][1])


    return out_v

def coloca_peca(field, action, piece):
    pos, rot = utils.translate_action(action, piece, Piece.pieces)

    collision_height = None

    for y in range(-1, len(field)):
        for block in Piece.pieces[piece][rot]:
            l = block // 4
            c = block % 4

            if y+l+1 == len(field):
                collision_height = y
                break

            if field[y+l+1][pos+c] == 1:
                collision_height = y
        if collision_height != None:
            break

    for block in Piece.pieces[piece][rot]:
        l = block // 4
        c = block % 4

        field[collision_height+l][pos+c] = 1

    return field


def cria_bloco(field, pile_height, height):
    #cria bloco pile_height*width no tabuleiro

    for i in range(pile_height, height):
        for j in range(len(field[pile_height])):
            field[i][j] = 1

    return field

def tira_peça(field, altered_columns, width, height):

    #tira peça do tabuleiro

    piece = random.randint(0, len(Piece.pieces)-1)
    action = random.randint(0, 4*width-1)

    pos, rot = utils.translate_action(action, piece, Piece.pieces)

    #acha lugares possíveis pra peça

    possible_y = []

    for y in range(-1, height):
        top_most_layer = 4*[4]
        collided = False
        preso = False
        interfere = False
        for block in Piece.pieces[piece][rot]:
            l = block // 4
            c = block % 4

            if pos+c < 0 or pos+c >= width:
                return None

            if y+l >= height:
                break

            if field[y+l][pos+c] == 1:
                collided = True

            if pos+c in altered_columns and field[y+l][pos+c] == 0:
                interfere = True

            if y+l-1 < 0:
                break

            if not (l-1)*4+c in Piece.pieces[piece][rot] and field[y+l-1][pos+c] == 1:
                preso = True
                break

        if collided and not preso and not interfere:
            possible_y.append(y)

    if len(possible_y) == 0:
        return None

    chosen_y = random.sample(possible_y, 1)[0]
    columns_used = 4*[0]


    #abre buraco pra peça
    for block in Piece.pieces[piece][rot]:
        l = block // 4
        c = block % 4

        if (chosen_y+l < 0) or (chosen_y+l >= height):
            #print("board overriden, y = ", chosen_y+l)
            return None

        field[chosen_y+l][pos+c] = 0
        columns_used[c] = 1

    used_columns = []
    for i in range(len(columns_used)):
        if columns_used[i] == 1:
            used_columns.append(pos+i)


    return (field, action, piece), used_columns

def torna_irregular(field, pile_height, used_columns, max_height, height):

    for i in range(len(field[0])):
        if not i in used_columns:
            new_height = pile_height - random.randint(0, 3)
            new_height = max(max_height, new_height)
            for j in range(new_height, height):
                field[j][i] = 1

    return field


def esburaca(field, pile_height, width, height):

    for i in range(pile_height+1, height):          #cria buracos
        holes = int(random.gauss(2.5, 1))
        holes = max(1, holes)
        holes = min(width//2, holes)

        for j in range(holes):
            field[i][random.randint(0, width-1)] = 0

    return field



def generate_empty_field(width, height):
    field = [ [ 0 for i in range(width) ] for j in range(height) ]
    return field


def copia_alteracoes(field_s, field_t, pile_height, altered_columns):
    for i in range(len(field_s)):
        for j in range(len(field_s[0])):
            if not i == pile_height or (j in altered_columns and i < pile_height):
                field_t[i][j] = field_s[i][j]

    return field_t


if __name__ == '__main__':
    state, piece, action = generate_experience_db(10, 20, 1, 10)

    if len(state) == 0:
        print("failed to generate field, try again")
        exit(0)

    for i in range(len(state)):
        utils.display_field(state[i], np.argmax(action[i]), utils.piece_num(piece[i]), Piece.pieces)
        print(np.argmax(action[i]))
        print(utils.translate_action(np.argmax(action[i]), utils.piece_num(piece[i]), Piece.pieces))
        print("piece: ", utils.piece_num(piece[i]))
        print(piece[i])
        print("entry num = ", i)

    #aux = generate_experience_db(10, 20, 100000)
