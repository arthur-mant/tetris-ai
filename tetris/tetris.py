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
    field = []
    height = 0
    width = 0
    fps = 0

    state = "start"
    piece = None
    next_piece = None

    def __init__(self, height, width, field=None):      #should be at least 4x4
        self.height = height
        self.width = width
        if bool(field):
            self.field = field
        else:
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
            self.state = "gameover"

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


class GameRun:

    done = False
    clock = pygame.time.Clock()
    fps = 60
    game = None
    counter = 0

    keyb = None
    queue_i = None
    screen_i = None
    pressing_down = False
    true_fps = 1

    def __init__(self, game, fps, use_screen=True, use_keyboard=False):
        pygame.init()
        self.game = game
        self.fps = fps

        if bool(use_screen):
            self.screen_i = screen.Screen(pygame, 500, 500, 100, 60, 20)
        if bool(use_keyboard) and bool(use_screen):
            self.keyb = interface_keyboard.Keyboard()
        else:
            self.queue_i = queue_interface.interface_queue()

    def run_frame(self):
        if self.game.piece is None:
            self.game.new_piece()
        self.counter += 1
        if self.counter > 100000:
            self.counter = 0

        if self.counter % (self.fps // (2*self.game.level)) == 0 or self.pressing_down:
            if self.game.state == "start":
                self.game.go_down()

        if bool(self.keyb):
            self.done, self.pressing_down = self.keyb.get_event_from_keyboard(pygame, self.game, self.pressing_down)
        elif bool(self.queue_i):
            self.queue_i.exec_command(self.game)
        else:
            print("ERROR: NO INPUT")

        if bool(self.screen_i):
            self.screen_i.update_screen(self.game)

        self.game.fps = self.true_fps = 1000 // self.clock.tick(self.fps)

#        if self.game.state == "gameover" and bool(self.queue_i):
#            self.done = True

        if self.done:
            self.close_game()
            return False

        return True

    def close_game(self):
        pygame.quit()


if __name__ == '__main__':

    game_run = GameRun(Tetris(20,10), 60, use_screen=True, use_keyboard=True)

    while game_run.run_frame():
        pass
