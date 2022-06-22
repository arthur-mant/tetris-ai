import heuristics

def get_state(game):
    #print("getting state")
    if game.field == None or game.piece == None or game.next_piece == None:
        print("ERROR: Trying to get board state but something is not initialized")
        return None

    holes, lines_cleared = heuristics.hole_number(game.field)
    abs_height = heuristics.absolute_height(game.field)
    bumpiness = heuristics.cumulative_height_difference(game.field)


    #return [game.piece.y, game.piece.x, game.piece.type, game.next_piece.type,
    return [game.piece.type, game.next_piece.type,
            holes, lines_cleared, abs_height, bumpiness]


def num_to_action(game, num):
    switch = {
        0: game.rotate,
        1: game.go_down,
        2: game.go_left,
        3: game.go_right
    }

    return switch.get(num, "Invalid input")
