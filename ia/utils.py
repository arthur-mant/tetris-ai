import copy
import numpy as np

def get_state(game, input_shape):
    #print("getting state")
    if game.field == None or game.piece == None or game.next_piece == None:
        print("ERROR: Trying to get board state but something is not initialized")
        return None

    original_field = []
    for i in range(len(game.field)):
        aux = []
        for j in range(len(game.field[0])):
            if game.field[i][j] == -1:
                aux.append(0)
            else:
                aux.append(1)
        original_field.append(aux)

    return [np.reshape(original_field, [1]+input_shape[0]), np.reshape(get_piece_vector(game), [1]+input_shape[1])]


def generate_all_fields(original_field, piece, piece_v):

    all_possible_fields = []
    valid_v = []
    rot_size = len(piece_v[piece])
    for i in range(10*rot_size):
        aux_field = copy.deepcopy(original_field)
        x = (i // rot_size) -2
        rot = i % rot_size
        stop = False
        invalid = False
        for y in range(20):
            for block in piece_v[piece][rot]:
                l = block // 4
                c = block % 4
                if x+c < 0 or x+c >= 10 or y+l <= 0:
                    invalid = True
                    break
                if y+l >= 20 or aux_field[y+l][x+c] == 1:
                    stop = True

            if invalid:
                break

            if stop:
                for block in piece_v[piece][rot]:
                    l = block // 4
                    c = block % 4
                    if aux_field[y+l-1][x+c] == 1:
                        print("ERROR: Trying to override block when making field list")
                    aux_field[y+l-1][x+c] = 1
                break
        all_possible_fields.append(aux_field)
        valid_v.append(not invalid)

    return all_possible_fields, valid_v


def get_piece_vector(game):

    num_pieces = len(game.piece.pieces)

    v = (num_pieces-1)*[0]

    for i in range(0, num_pieces-1):
        if game.piece.type == i:
            v[i] = 1

    return v

def display_field(field, action, piece, pieces):

    pos, rot = translate_action(action, piece, pieces)

    piece_pos = []

    for block in pieces[piece][rot]:
        l = block // 4
        c = block % 4

        piece_pos.append((l, pos+c))

    for i, line in enumerate(field):
        aux = ""
        for j, value in enumerate(line):
            if (i, j) in piece_pos:
                aux += "1 "
            elif value == 0:
                aux += "  "
            else:
                aux += "0 "
        print("| ", aux, "| ", i)

    print((5+2*len(field[0]))*'-')
    print("   0 1 2 3 4 5 6 7 8 9")

def translate_action(action, piece, pieces):
    rot_num = len(pieces[piece])

    aux = int(action * rot_num/4)

    rot = aux % rot_num
    pos = (aux // rot_num)-1

    return pos, rot

def piece_num(piece_v):
    aux = np.argmax(piece_v)
    if piece_v[aux] == 0:
        return len(piece_v)+1-1
    return aux
