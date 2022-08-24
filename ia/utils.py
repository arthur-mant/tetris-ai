import copy

def get_state(game):
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

    return original_field


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


def num_to_action(game, num):
    switch = {
        0: game.rotate,
        1: game.go_down,
        2: game.go_left,
        3: game.go_right
    }

    return switch.get(num, "Invalid input")

def display_field(field):
    for i in field:
        aux = ""
        for j in i:
            if j == 0:
                aux += "  "
            else:
                aux += "0 "
        print("| ", aux, "|")

    print((5+2*len(field[0]))*'-')
