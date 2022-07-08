def get_state(game):
    #print("getting state")
    if game.field == None or game.piece == None or game.next_piece == None:
        print("ERROR: Trying to get board state but something is not initialized")
        return None

    field = [ [ 0 for i in range(len(game.field[0])) ] for j in range(4) ]

    for i in game.piece.image():
        field[i//4][i%4] = 1
    for i in game.next_piece.image():
        field[i//4][4+(i%4)] = 1


    for i in range(len(game.field)):
        aux = []
        for j in range(len(game.field[0])):
            if game.field[i][j] == -1:
                aux.append(0)
            else:
                aux.append(1)
        field.append(aux)

    print("types: ", game.piece.type, ", ", game.next_piece.type)
    print(field)

    return field

def num_to_action(game, num):
    switch = {
        0: game.rotate,
        1: game.go_down,
        2: game.go_left,
        3: game.go_right
    }

    return switch.get(num, "Invalid input")
