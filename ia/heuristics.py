

def score(field, lines, weights):
    functions = [hard_hole_number, soft_hole_number, absolute_height, cumulative_height_difference, lines_cleared, has_i_valley, i_valley_pos_relative_to_center]
    score = 0
    for i in range(len(functions)):
        print(functions[i], ": ", functions[i](field, lines))
        score += weights[i]*pow(functions[i](field, lines), 2)
    return score

def hard_hole_number(field, lines):
    holes = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == -1:
                blocked = (False, False, False)
                if i-1 > 0 and field[i-1][j] > -1:
                    blocked = (True, blocked[1], blocked[2])
                if j-1 < 0 or field[i][j-1] > -1:
                    blocked = (blocked[0], True, blocked[2])
                if j+1 >= len(field[i]) or field[i][j+1] > -1:
                    blocked = (blocked[0], blocked[1], True)

                if blocked[0] and blocked[1] and blocked[2]:
                    holes += 1

    return holes

def soft_hole_number(field, lines):
    holes = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == -1 and i-1 > 0 and field[i-1][j] > -1:
                holes += 1

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
    return lines*lines

def has_i_valley(field, lines):
    _unused, aux = check_i_valley(field)
    if aux == 1:
        return 1
    return 0

def i_valley_pos_relative_to_center(field, lines):
    pos, num = check_i_valley(field)
    if num != 1:
        return -1       #mudar?
    if pos < len(field[0])//2:
        return (len(field[0])//2)+1-pos
    else:
        return pos - (len(field[0])//2)



#auxiliary functions:

def get_height(field, column):
    for i in range(len(field)):
        if field[i][column] > -1:
            return len(field) - i
    return 0

def check_i_valley(field):
    pos = -1
    num = 0
    for j in range(len(field[0])):
        if ((j - 1) < 0 or abs(get_height(field, j-1) - get_height(field, j)) >= 4) and ((j+1) >= len(field[0]) or abs(get_height(field, j) - get_height(field, j+1)) >= 4):
            pos = j
            num += 1
    return pos, num
