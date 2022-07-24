import sys
sys.path.insert(0, '/home/martinelli/tetris-ia/tetris')
from tetris import Piece
import utils
import random
import copy
import time

def generate_experience_db(width, height, num):

    exp_db = []

    begin_time = time.time()
    #aux_time = time.time()

    for i in range(num):
        #if i % 1000 == 0:
        #    print("time for ", i//1000, "th batch of 1000: ", time.time()-aux_time, "s")
        #    aux_time = time.time()
        aux = generate_plain_field(
            width, height,
            random.randint(4, height-2),
            random.gauss(2, 0.75),
            int(random.gauss(2, 1))
        )
        exp_db.append(aux)

    print("Took ", time.time()-begin_time, "s to generate exp db")

    return exp_db

def generate_plain_field(width, height, pile_height, bump_factor, mean_holes):

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
    if (mean_holes >= width) or (mean_holes <= 0):
        #print("ERROR: invalid board mean holes per line: ", mean_holes)
        #return None
        mean_holes = 1


    field = generate_empty_field(width, height)

    last_column_height = pile_height

    columns_heights = []

    for i in range(width):
        last_column_height = last_column_height+int(random.gauss(0, bump_factor))
        last_column_height = max(1, last_column_height)
        last_column_height = min(height, last_column_height)
        columns_heights.append(last_column_height)

    for j in range(len(columns_heights)):
        for i in range(columns_heights[j], height):
            #print(i, ", ", j)
            field[i][j] = 1

    #cortando uma peça fora
    possible_cuts = []
    for x in range(-2, width):
        for piece in range(len(Piece.pieces)):
            for rot in range(len(Piece.pieces[piece])):
                if can_cut_piece(field, x, Piece.pieces[piece][rot]):
                    possible_cuts.append((x, piece, rot))

    if len(possible_cuts) <= 0:
        return None

    chosen_cut = random.sample(possible_cuts, 1)[0]

    #print(chosen_cut)

    #x = chosen_cut[0]
    #piece = chosen_cut[1]
    #rot = chosen_cut[2]

    (x, piece, rot) = chosen_cut

    end_field = copy.deepcopy(field)

    for line in range(len(field)):
        correct_pos = True
        for block in Piece.pieces[piece][rot]:
            i = block//4
            j = block % 4

            if field[line+i][x+j] != 1:
                correct_pos = False
        if correct_pos:
            y = line
            for block in Piece.pieces[piece][rot]:
                i = block // 4
                j = block % 4

                field[line+i][x+j] = 0
            break

    next_piece = Piece.pieces[random.randint(0, len(Piece.pieces)-1)][0]

    begin_field = draw_pieces(Piece.pieces[piece][0], next_piece) + field

    end_field = draw_pieces(
        next_piece,
        Piece.pieces[random.randint(0, len(Piece.pieces)-1)][0]
    ) + end_field

    action = 4*(x+1) + rot

    reward = height-y

    done = False

    return begin_field, action, reward, end_field, done

def can_cut_piece(field, x, piece):

    for line in range(len(field)):
        viable = True
        for block in piece:
            i = block//4
            j = block % 4

            if x+j < 0 or x+j >= len(field[0]) or line+i >= len(field):
                return False

            if field[line+i][x+j] != 1:
                viable = False

        if viable:
            for block in piece:
                j = block % 4

                for i in range(line+block//4, 0, -1):
                    if i < len(field):
                        if field[i][x+j] == 1 and not (4*(i-line)+j) in piece:
                            return False

            return True
    return False

def draw_pieces(piece1, piece2):

    field = [ [ 0 for i in range(10) ] for j in range(4) ]

    for block in piece1:
        i = block // 4
        j = block % 4

        field[i][j] = 1

    for block in piece2:
        i = block // 4
        j = block % 4

        field[i][4+j] = 1

    return field

def generate_empty_field(width, height):
    field = [ [ 0 for i in range(width) ] for j in range(height) ]
    return field


if __name__ == '__main__':
    #state, action, reward, next_state, done = generate_experience_db(10, 20, 1)[0]
    #utils.display_field(state)
    #print("")
    #utils.display_field(next_state)

    aux = generate_experience_db(10, 20, 100000)
