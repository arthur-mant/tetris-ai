def get_state(game):
    print("getting state")
    if game.field == None or game.piece == None or game.next_piece == None:
        print("ERROR: Trying to get board state but something is not initialized")
        return None

    field = []
    for i in range(len(game.field)):
        for j in range(len(game.field[0])):
            if game.field[i][j] == -1:
                field.append(0)
            else:
                field.append(1)

    piece = [0 for n in range(7)]
    piece[game.piece.type] = 1

    next_piece = [0 for n in range(7)]
    next_piece[game.next_piece.type] = 1

    return field+piece+next_piece

def num_to_action(game, num):
    switch = {
        0: game.rotate,
        1: game.go_down,
        2: game.go_left,
        3: game.go_right
    }

    return switch.get(num, "Invalid input")
