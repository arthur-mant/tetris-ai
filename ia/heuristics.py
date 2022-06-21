
def hole_number(field):
    holes = 0
    lines_cleared = 0
    for i in range(len(field)):
        local_holes = 0
        for j in range(len(field[i])):
            if field[i][j] == -1 and i-1 > 0 and field[i-1][j] > -1:
                local_holes += 1
                holes += 1

        if local_holes == 0:
            lines_cleared += 1

    return holes, lines_cleared

def absolute_height(field):
    max_height = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] > -1:
                max_height = max(len(field)-i, max_height)

    return max_height

def cumulative_height_difference(field):
    height = -1
    height_sum = 0
    for j in range(len(field[0])):
        i = get_height(field, j)
        if height != -1:
            height_sum += abs(i - height)
        height = i

    return height_sum


#def has_i_valley_on_border(field, lines):
#    if get_height(field, 1) - get_height(field, 0) >= 4:
#        return 1
#    if get_height(field, len(field[0])-2) - get_height(field, len(field[0])-1) >= 4:
#        return 1
#    return 0



#auxiliary functions:

def get_height(field, column):
    for i in range(len(field)):
        if field[i][column] > -1:
            return len(field) - i
    return 0

