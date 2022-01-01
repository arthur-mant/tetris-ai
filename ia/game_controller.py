import numpy
import tetris

class Controller:

    game = None

    def __init__(self, game):
        self.game = game

    def get_piece_shadow(self, x):
        y = self.game.piece.y

        collide = False
        while not collide:
            y += 1
            for block in self.game.piece.image():
                i = block // 4
                j = block % 4
                if (self.game.field[y+i][x+j] == -1):
                    collide = True
                    y -= 1

        return y

    def get_path(self, x, y, rot):
        visitados = [ [ list(range(len(self.game.piece.pieces[self.game.piece.type]))) for i in range(self.game.width) ] for j in range(self.game.height) ]
        #print(visitados)
        path, x1, y1 = self.create_path(x, y, rot, visitados)

        if path == None:
            #print("(", x,", ", y, ", ", rot, ") has no path!")
            return None

        for i in range(y1, 0, -1):
            path = ["B"]+path

        for i in range(x1, (self.game.width//2)-2, -1):
            path = ["D"]+path
        for i in range(x1, (self.game.width//2)-2, 1):
            path = ["E"]+path

        return path

    def create_path(self, x, y, rot, visitados):

        #condições de base
        if not rot in visitados[y][x]:
            return None, -1, -1
        visitados[y][x].remove(rot)

        for block in self.game.piece.pieces[self.game.piece.type][rot]:
            i = block // 4
            j = block % 4
            if y+i < 0 or y+i >= self.game.height or x+j < 0 or x+j >= self.game.width or (self.game.field[y+i][x+j] != -1):
                #print("(", x, ", ", y, ", ", rot, ") is blocked")
                return None, -1, -1

        is_free = True
        for block in self.game.piece.pieces[self.game.piece.type][rot]:
            i = block // 4
            j = block % 4
            for k in range(y, 0, -1):
                if (self.game.field[k+i][x+j] > -1):
                    is_free = False

        if is_free:
            #print("(", x, ", ", y, ", ", rot, ") is free")
            return [], x, y

        #recursão

        aux, x1, y1 = self.create_path(x, y+1, rot, visitados)
        if aux != None:
            return aux+["B"], x1,  y1
        aux, x1, y1 = self.create_path(x-1, y, rot, visitados)
        if aux != None:
            return aux+["E"], x1, y1
        aux, x1, y1 = self.create_path(x+1, y, rot, visitados)
        if aux != None:
            return aux+["D"], x1, y1
        aux, x1, y1 = self.create_path(x, y, (rot-1) % len(self.game.piece.pieces[self.game.piece.type]), visitados)
        if aux != None:
            return aux+["R"], x1, y1
        return None, -1, -1

    def get_all_possible_pos(self):         #returns list of tuple(x, y, rot, path)
        return_list = []

        for y in range(-2, self.game.height):
            for x in range(-2, self.game.width):
                for rot in range(len(self.game.piece.pieces[self.game.piece.type])):
                    placeable = True
                    has_block_under = False
                    for block in self.game.piece.pieces[self.game.piece.type][rot]:
                        i = block // 4
                        j = block % 4
                        if (y+i >= self.game.height) or (x+j >= self.game.width) or (x+j < 0) or (self.game.field[y+i][x+j] > -1):
                            placeable = False


                        if placeable and ((y+i+1 > self.game.height-1) or (self.game.field[y+i+1][x+j] > -1)):
                            has_block_under = True

                    if placeable and has_block_under:
                        return_list.append((x, y, rot, self.get_path(x, y, rot)))
#        for elem in return_list:
#            if elem[3] == None:
#                return_list.remove(elem)
        return return_list

    def path_to_command(self, path):
        for i in path:
            if i == "E":
                self.game.interface_queue.move(-1)
            if i == "D":
                self.game.interface_queue.move(1)
            if i == "R":
                self.game.interface_queue.rotate(1)
            if i == "B":
                self.game.interface_queue.down(1)


    def put_piece(self, rotation, x, y, path=None):

        hard_drop = (y == self.get_piece_shadow(x))

        if hard_drop:
            self.game.interface_queue.move(x - self.game.piece.x)
            self.game.interface_queue.rotate(rotation)
            self.game.interface_queue.hard_drop()

        else:
            if path:
                self.path_to_command(path)
            else:
                path_to_command(get_path(x, y, rotation))

