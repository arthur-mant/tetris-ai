def get_state(game):
    #print("getting state")
    if game.field == None or game.piece == None or game.next_piece == None:
        print("ERROR: Trying to get board state but something is not initialized")
        return None

    field = []

    for i in range(len(game.field)):
        aux = []
        for j in range(len(game.field[0])):
            if game.field[i][j] == -1:
                aux.append(0)
            else:
                aux.append(1)
        field.append(aux)

    return field

def hot_encode(piece_type):
    v = [ 0 for i in range(6)]
    if piece_type < 6:
        v[piece_type] = 1
    return v

def num_to_action(game, num):
    switch = {
        0: game.rotate,
        1: game.go_down,
        2: game.go_left,
        3: game.go_right
    }

    return switch.get(num, "Invalid input")
