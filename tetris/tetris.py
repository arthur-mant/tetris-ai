import pygame
import random
import screen
import interface_keyboard
import queue_interface

class Piece:
    x = 0
    y = 0

    pieces = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[1, 2, 5, 9], [4, 5, 6, 10], [1, 5, 9, 8], [0, 4, 5, 6]],
        [[1, 2, 6, 10], [3, 5, 6, 7], [2, 6, 10, 11], [5, 6, 7, 9]],
        [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]],
        [[1, 2, 5, 6]],
        [[0, 1, 5, 6], [2, 6, 5, 9]],
        [[1, 2, 4, 5], [1, 5, 6, 10]]
    ]


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.pieces) - 1)
        self.rotation = 0

    def image(self):
        return self.pieces[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation+1) % len(self.pieces[self.type])


class Tetris:
    level = 1
    score = 0
    lines = 0
    pieces = -2
    fps = 0
    field = []
    height = 0
    width = 0

    state = "start"
    piece = None
    next_piece = None

    interface_queue = None

    def __init__(self, height, width):      #should be at least 4x4
        self.height = height
        self.width = width
        self.interface_queue = queue_interface.interface_queue()
        self.field = [ [ -1 for i in range(width) ] for j in range(height) ]

    def new_piece(self):
        self.piece = self.next_piece
        self.next_piece = Piece((self.width//2)-2,0)
        self.pieces += 1

    def intersects(self):
        intersection = False

        for block in self.piece.image():
            i = block//4
            j = block%4

            if i+self.piece.y > self.height-1 or \
                j+self.piece.x > self.width-1 or \
                j+self.piece.x < 0 or \
                self.field[i+self.piece.y][j+self.piece.x] > -1:
                    intersection = True
        return intersection

    def freeze(self):
        for block in self.piece.image():
            i = block//4
            j = block%4
            self.field[i+self.piece.y][j+self.piece.x] = self.piece.type
        self.break_lines()
        self.new_piece()
        if self.intersects():
            game.state = "gameover"

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            holes = 0
            for j in range(self.width):
                if self.field[i][j] == -1:
                    holes += 1
            if holes == 0:
                lines += 1
                for k in range(i, 1, -1):
                    for l in range(self.width):
                        self.field[k][l] = self.field[k-1][l]
        self.score += lines*lines
        self.lines += lines

    def hard_drop(self):
        while not self.intersects():
            self.piece.y += 1
        self.piece.y -=1
        self.freeze()

    def go_down(self):
        self.piece.y += 1
        if self.intersects():
            self.piece.y -= 1
            self.freeze()

    def go_side(self, dx):
        old_x = self.piece.x
        self.piece.x += dx
        if self.intersects():
            self.piece.x = old_x

    def rotate(self):
        old_rotation = self.piece.rotation
        self.piece.rotate()
        if self.intersects():
            self.piece.rotation = old_rotation

    def level_up(self):
        self.level += 1

if __name__ == '__main__':

    pygame.init()

    done = False
    clock = pygame.time.Clock()
    fps = 60
    game = Tetris(20, 10)
    counter = 0

    screen_i = screen.Screen(pygame, 500, 500, 100, 60, 20)
    keyb = interface_keyboard.Keyboard()

    pressing_down = False
    true_fps = 1

    while not done:

        if game.piece is None:
            game.new_piece()
        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (fps // (2*game.level)) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()

        done, pressing_down = keyb.get_event_from_keyboard(pygame, game, pressing_down)

        screen_i.update_screen(game)

        game.fps = 1000 // clock.tick(fps)

    pygame.quit()
