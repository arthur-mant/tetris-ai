
def get_state(game):

    if game.field == None or game.piece == None or game.next_piece == None:
        print("ERROR: Trying to get board state but something is not initialized")
        return None

    field = game.field.deepcopy()
    for i in len(field):
        for j in len(i):
            if field[i][j] == -1:
                field[i][j] = 0
            else:
                field = 1

    piece = [0 for n in range(7)]
    piece[game.piece] = 1

    next_piece = [0 for n in range(7)]
    next_piece[game.piece] = 1

    return field+piece+next_piece

def num_to_action(game, num):
    switch = {
        0: game.rotate
        1: game.go_down
        2: game.go_left
        3: game.go_right
    }

    return switch.get(num, "Invalid input")
