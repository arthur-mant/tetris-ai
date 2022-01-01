import random

def generate_plain_field(width, height, pile_height, mean_holes):

    field = [ [ -1 for i in range(width) ] for j in range(height) ]

    for y in range(height-1, height-1-pile_height, -1):
        holes = min(random.randint(1, int(1*mean_holes)), width-1)
        holes = max(holes, 1)
        for x in range(width):
            field[y][x] = 7
        for i in range(holes):
            field[y][random.randint(0, width-1)] = -1

    return field
