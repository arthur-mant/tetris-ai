import sys
sys.path.insert(0, '/home/martinelli/tetris-ia/tetris')
from tetris import Piece
import utils
import random
import copy
import time

def generate_experience_db(width, height, num):

    begin_time = time.time()
    #aux_time = time.time()

    aux_v = []
    for i in range(num):
        out = generate_plain_field(
            width, height,
            random.randint(4, height-5),
            int(random.gauss(2, 1))
        )

        aux_v = aux_v+out

    field_v = []
    dist_v = []
    for i in out:
        field_v.append(i[0])
        dist_v.append(i[1])

        #if i % 1000 == 0:
        #    print("time for ", i//1000, "th batch of 1000: ", time.time()-aux_time, "s")
        #    aux_time = time.time()

    print("Took ", time.time()-begin_time, "s to generate exp db with ", len(field_v), " entries")

    return field_v, dist_v

def generate_plain_field(width, height, pile_height, mean_holes):

    if (width <= 5):
        print("ERROR: board too narrow")
        return None
    if (height <= 5):
        print("ERROR: board too small")
        return None
    if (pile_height >= height) or (pile_height < 0):
        print("ERROR: invalid board pile_height: ", pile_height)
        return None
    if (mean_holes >= width) or (mean_holes <= 0):
        #print("ERROR: invalid board mean holes per line: ", mean_holes)
        #return None
        mean_holes = 1


    field = generate_empty_field(width, height)

    columns_heights = []

    for j in range(width):
        for i in range(pile_height, height):
            field[i][j] = 1

    for i in range(pile_height+5, height):
        holes = int(random.gauss(mean_holes, 0.5))
        holes = max(1, holes)
        holes = min(width//2, holes)

        for j in range(holes):
            field[i][random.randint(0, width-1)] = 0

    i = 0
    blocks = width*4
    out = []
    while blocks > 2 and field != None:
        i += 1
        field = cut_piece_out(field, pile_height)

        if field != None:
            #utils.display_field(field)
            out.append((copy.deepcopy(field), i))
        else:
            #print("field == None(?)")
            break

        blocks = 0
        for j in range(pile_height, pile_height+5):
            for k in range(width):
                blocks += field[j][k]

    return out

def cut_piece_out(field, top_line):
    possible_cuts = []
    for x in range(-2, len(field[0])):
        for piece in range(len(Piece.pieces)):
            for rot in range(len(Piece.pieces[piece])):
                if can_cut_piece(field, x, Piece.pieces[piece][rot], top_line):
                    possible_cuts.append((x, piece, rot))

    if len(possible_cuts) <= 0:
        return None

    chosen_cut = random.sample(possible_cuts, 1)[0]

    (x, piece, rot) = chosen_cut

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


    return field

def can_cut_piece(field, x, piece, top_line):

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
            has_block_under = False
            blocks_inside_tetris = 0
            for block in piece:
                j = block % 4

                for i in range(line+block//4, 0, -1):
                    if i < len(field):
                        if field[i][x+j] == 1 and not (4*(i-line)+j) in piece:
                            return False
                if line+block//4+1 < len(field) and field[line+block//4+1][x+j] == 1:
                    has_block_under = True

                if line+block//4 < top_line+4:
                    blocks_inside_tetris += 1


            return (has_block_under and blocks_inside_tetris >= 2)
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
    states, distances = generate_experience_db(10, 20, 1)

    for i in range(len(states)):
        utils.display_field(states[i])
        print(distances[i])

    #aux = generate_experience_db(10, 20, 100000)
