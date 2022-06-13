import copy

def get_state(game, field):
    #print("getting state")
    if field == None or game.piece == None or game.next_piece == None:
        print("ERROR: Trying to get board state but something is not initialized")
        return None

    board = []
    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] == -1:
                board.append(0)
            else:
                board.append(1)

    y_pos = [0 for n in range(20)]
    y_pos[game.piece.y+2] = 1

    x_pos = [0 for n in range(10)]
    x_pos[game.piece.x] = 1

    piece = [0 for n in range(7)]
    piece[game.piece.type] = 1

    next_piece = [0 for n in range(7)]
    next_piece[game.next_piece.type] = 1

    rotation = [0 for n in range(4)]
    rotation[game.piece.rotation] = 1

    return board+x_pos+y_pos+rotation+piece+next_piece

def num_to_action(game, num):
    switch = {
        0: game.rotate,
        1: game.go_down,
        2: game.go_left,
        3: game.go_right
    }

    return switch.get(num, "Invalid input")


def get_all_states(game):   #returns list of board positions
    states = []

    for x in range(game.width):
        for rot in range(len(game.piece.pieces[game.piece.type])):
            placeable = True
            for block in game.piece.pieces[game.piece.type][rot]:
                i = block // 4
                j = block % 4
                if (x+j >= game.width) or (-2+i >= 0 and (game.field[-2+i][x+j] > -1)):
                    placeable = False
            if placeable:
                y = -2
                has_block_under = False
                while not has_block_under:
                    for block in game.piece.pieces[game.piece.type][rot]:
                        i = block // 4
                        j = block % 4
                        if (y+i+1 >= 0 and game.field[y+i+1][x+j] == -1):
                            has_block_under = True
                    y += 1

                states.append((x, y, rot))

    return states

def coordinates_to_field(game, coordinates):

    x = coordinates[0]
    y = coordinates[1]
    rot = coordinates[2]

    field = copy.deepcopy(game.field)

    for block in game.piece.pieces[game.piece.type][rot]:
        i = block // 4
        j = block % 4

        if field[y+i][x+j] != -1:   #remover depois
            print("ERROR: trying to create field but overwrote something")

        field[y+i][x+j] = game.piece.type

    return field
