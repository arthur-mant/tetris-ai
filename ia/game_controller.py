import numpy
import copy
import tetris

class Controller:

    game_run = None

    def __init__(self, game_run):
        self.game_run = game_run

    def get_piece_shadow(self, x, rot):
        y = self.game_run.game.piece.y

        collide = False
        while not collide:
            y += 1
            for block in self.game_run.game.piece.pieces[self.game_run.game.piece.type][rot]:
                i = block // 4
                j = block % 4
                if y+i >= self.game_run.game.height or (self.game_run.game.field[y+i][x+j] > -1):
                    collide = True
                    y -= 1
                    #print("y+i = ", y+i)

        return y

    def get_path(self, x, y, rot):
        visitados = [ [ list(range(len(self.game_run.game.piece.pieces[self.game_run.game.piece.type]))) for i in range(self.game_run.game.width) ] for j in range(self.game_run.game.height) ]
        #print(visitados)
        path, x1, y1 = self.create_path(x, y, rot, visitados, ((self.game_run.game.width//2)-2, 0, 0))

        if path == None:
            #print("(", x,", ", y, ", ", rot, ") has no path!")
            return None

        last_right = -1
        last_left = -1
        i = 0
        while (i < (len(path))):
            if path[i] == "E":
                last_left = i
            if path[i] == "D":
                last_right = i
            if path[i] == "B":
                last_right = last_left = -1
            if last_right >= 0 and path[i] == "E":
                del path[i]
                del path[last_right]
                last_right = last_left = -1
                i = -1
            if last_left >= 0 and path[i] == "D":
                del path[i]
                del path[last_left]
                last_right = last_left = -1
                i = -1
            i+=1

        path = path+["B"]

        return path

    def create_path(self, x, y, rot, visitados, obj):

        #condições de base
        if not rot in visitados[y][x]:
            return None, -1, -1
        visitados[y][x].remove(rot)

        for block in self.game_run.game.piece.pieces[self.game_run.game.piece.type][rot]:
            i = block // 4
            j = block % 4
            if y+i < 0 or y+i >= self.game_run.game.height or x+j < 0 or x+j >= self.game_run.game.width or (self.game_run.game.field[y+i][x+j] != -1):
                #print("(", x, ", ", y, ", ", rot, ") is blocked")
                return None, -1, -1

#        print((x, y, rot))
        if ((x, y, rot) == obj):
            return [], x, y

        #recursão

        aux, x1, y1 = self.create_path(x, y-1, rot, visitados, obj)
        if aux != None:
            return aux+["B"], x1,  y1
        aux, x1, y1 = self.create_path(x+1, y, rot, visitados, obj)
        if aux != None:
            return aux+["E"], x1, y1
        aux, x1, y1 = self.create_path(x-1, y, rot, visitados, obj)
        if aux != None:
            return aux+["D"], x1, y1
        aux, x1, y1 = self.create_path(x, y, (rot-1) % len(self.game_run.game.piece.pieces[self.game_run.game.piece.type]), visitados, obj)
        if aux != None:
            return aux+["R"], x1, y1
        return None, -1, -1

    def get_all_possible_pos(self, field, piece):         #returns list of tuple(x, y, rot, path)
        return_list = []

        for y in range(-2, len(field)):
            for x in range(-2, len(field[0])):
                for rot in range(len(self.game_run.game.piece.pieces[piece])):
                    placeable = True
                    has_block_under = False
                    for block in self.game_run.game.piece.pieces[piece][rot]:
                        i = block // 4
                        j = block % 4
                        if (y+i >= len(field)) or (x+j >= len(field[0])) or (x+j < 0) or (field[y+i][x+j] > -1):
                            placeable = False


                        if placeable and ((y+i+1 > len(field)-1) or (field[y+i+1][x+j] > -1)):
                            has_block_under = True

                    if placeable and has_block_under:
                        return_list.append((x, y, rot, self.get_path(x, y, rot)))

        return_list = [elem for elem in return_list if elem[3] != None]

        return return_list

    def path_to_command(self, path):
        for i in path:
            if i == "E":
                self.game_run.queue_i.move(-1)
            if i == "D":
                self.game_run.queue_i.move(1)
            if i == "R":
                self.game_run.queue_i.rotate(1)
            if i == "B":
                self.game_run.queue_i.go_down(1)


    def put_piece(self, rotation, x, y, path=None):

        if not bool(path):
            path = self.get_path(x, y, rotation)

        only_down = False
        for elem in path:
            if elem == "B":
                only_down = True
            if only_down and elem != "B":
                only_down = False
                break

        rotation_clusters = 0
        for i in range(1, len(path)):
            if path[i] == "R" and path[i-1] != "R":
                rotation_clusters += 1


        if only_down and rotation_clusters <= 1:
            self.game_run.queue_i.rotate(rotation)
            self.game_run.queue_i.move(x - self.game_run.game.piece.x)
            self.game_run.queue_i.hard_drop()

        else:
            print("following path")
            self.path_to_command(path)

    def simulate_piece(self, x, y, rotation):
        new_field = copy.deepcopy(self.game_run.game.field)
        for block in self.game_run.game.piece.pieces[self.game_run.game.piece.type][rotation]:
            i = block // 4
            j = block % 4
            if self.game_run.game.field[y+i][x+j] > 0:
                print("ERROR: TRIED TO OVERWRITE BLOCK")
                return None
            new_field[y+i][x+j] = self.game_run.game.piece.type

        lines = 0
        for i in range(len(new_field)):
            hole = False
            for j in range(len(new_field[i])):
                if new_field[i][j] == -1:
                    hole = True
            if not hole:
                lines += 1
                for k in range(i, 1, -1):
                    for j in range(len(new_field[i])):
                        new_field[k][j] = new_field[k-1][j]

        return new_field, lines

    def check_if_right_position(self, new_field):
        if not bool(new_field):
            return True

        print("predicted field:")
        for i in range(self.game_run.game.height):
            for j in range(self.game_run.game.width):
                print(new_field[i][j])
            print()
        print("actual field:")
        for i in range(self.game_run.game.height):
            for j in range(self.game_run.game.width):
                print(self.game_run.game.field[i][j])
            print()

        for i in range(self.game_run.game.height):
            for j in range(self.game_run.game.width):
                if self.game_run.game.field[i][j] != new_field[i][j]:
                    #print("ERROR: PREDICTED FIELD DIFFERENT FROM REAL ONE")
                    print(i, ", ", j)
                    raise Exception("ERROR: PREDICTED FIELD DIFFERENT FROM REAL ONE")
                    return False
        return True
