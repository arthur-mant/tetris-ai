

def score(field, weights):
    functions = [hard_hole_number, soft_hole_number, absolute_height]
    score = 0
    for i in range(len(functions)):
        #print(functions[i], ": ", functions[i](field))
        score += weights[i]*functions[i](field)
    return score

def hard_hole_number(field):
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

def soft_hole_number(field):
    holes = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == -1 and i-1 > 0 and field[i-1][j] > -1:
                holes += 1

    return holes

def absolute_height(field):
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] > -1:
                return (len(field)-i)

    return (len(field))
