

def score(field, lines, weights):
    functions = [hole_number, absolute_height, cumulative_height_difference, lines_cleared, has_i_valley_on_border, invades_spawn_area]
    score = 0
    for i in range(len(functions)):
        print(functions[i], ": ", functions[i](field, lines))
        score += weights[i]*pow(functions[i](field, lines), 2)
    return score

def hole_number(field, lines):
    holes = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == -1 and i-1 > 0 and field[i-1][j] > -1:
                k = i
                end_hole = False
                while k < len(field) and not end_hole:
                    if field[k][j] == -1:
                        holes += 1
                    else:
                        end_hole = True
                    k = k+1

    return holes

def absolute_height(field, lines):
    max_height = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] > -1:
                max_height = max(len(field)-i, max_height)

    return max_height

def cumulative_height_difference(field, lines):
    height = -1
    height_sum = 0
    for j in range(len(field[0])):
        i = get_height(field, j)
        if height != -1:
            height_sum += abs(i - height)
        height = i

    return height_sum

def lines_cleared(field, lines): #mexer no expoente?
    total = 0
    for elem in lines:
        total = total + elem*elem
    return total

def has_i_valley_on_border(field, lines):
    if get_height(field, 1) - get_height(field, 0) >= 4:
        return 1
    if get_height(field, len(field[0])-2) - get_height(field, len(field[0])-1) >= 4:
        return 1
    return 0


def invades_spawn_area(field, lines):
    for i in range(4):
        for j in range(0, len(field[0])):
            if field[i][j] > -1:
                return 4-i
    return 0

#auxiliary functions:

def get_height(field, column):
    for i in range(len(field)):
        if field[i][column] > -1:
            return len(field) - i
    return 0

