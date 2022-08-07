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

    all_possible_fields = []
    rot_size = len(game.piece.pieces[game.piece.type])
    for i in range(10*rot_size):
        aux_field = copy.deepcopy(original_field)
        x = (i // rot_size) -2
        rot = i % rot_size
        for y in range(20):
            for block in game.piece.pieces[rot]:
                l = block // 4
                c = block % 4
                if aux_field[y+l][x+c] == 1:
                    stop = True
            if stop:
                for block in game.piece.pieces[rot]:
                    l = block // 4
                    c = block % 4
                    if aux_field[y+l-1][x+c] == 1:
                        print("ERROR: Trying to override block when making field list")
                    aux_field[y+l-1][x+c] = 1
                    break


    return all_possible_fields

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
