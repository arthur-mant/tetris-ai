import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

colors = [          #adicionar cores
    (0, 0, 204),
    (0, 204, 0),
    (204, 0, 0),
    (102, 0, 204),
    (255, 153, 0),
    (255, 0, 255),
    (0, 204, 255)
]

class Figure:
    x = 0
    y = 0

    figures = [
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
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = colors[self.type]
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation+1) % len(self.figures[self.type])


class Tetris:
    level = 1
    score = 0
    lines = 0
    field = []
    height = 0
    width = 0

    state = "start"
    x = 100
    y = 60
    zoom = 20
    figure = None

    def __init__(self, height, width):      #should be at least 4x4
        self.height = height
        self.width = width
        self.field = [ [ -1 for i in range(width) ] for j in range(height) ]    #[[-1]*(width)]*(height)
        #print(self.field)

    def new_figure(self):
        self.figure = Figure((self.width//2)-2,0)

    def intersects(self):
        intersection = False

#        for i in range(4):
#            for j in range(4):
#                if i*4+j in self.figure.image():
#                    print(self.field[i+self.figure.y][j+self.figure.x])
#                    if i+self.figure.y > self.height-1 or \
#                         j+self.figure.x > self.width-1 or \
#                         j+self.figure.x < 0 or \
#                         self.field[i+self.figure.y][j+self.figure.x] > 0:
#                             intersection = True

        for block in self.figure.image():
            i = block//4
            j = block%4
#            print("next:")
#            print(i+self.figure.y)
#            print(j+self.figure.x)
#            print(self.field[i+self.figure.y][j+self.figure.x])
            if i+self.figure.y > self.height-1 or \
                j+self.figure.x > self.width-1 or \
                j+self.figure.x < 0 or \
                self.field[i+self.figure.y][j+self.figure.x] > -1:
                    intersection = True
        return intersection

    def freeze(self):
#        print("before:")
#        print(self.field)
        for block in self.figure.image():
            i = block//4
            j = block%4
            print("next:")
            print(i+self.figure.y, j+self.figure.x)
            print(self.field[i+self.figure.y][j+self.figure.x])
            print(self.figure.type)
            print("before:")
            print(self.field)
            self.field[i+self.figure.y][j+self.figure.x] = self.figure.type
            print("after:")
            print(self.field)
        self.break_lines()
        self.new_figure()
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
                print("eliminate line")
                lines += 1
                for k in range(i, 1, -1):
                    for l in range(self.width):
                        self.field[k][l] = self.field[k-1][l]
        self.score += lines*lines
        self.lines += lines

    def hard_drop(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -=1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        print("trying to rotate")
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

pygame.init()

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

done = False
clock = pygame.time.Clock()
fps = 60
game = Tetris(20, 10)
counter = 0

pressing_down = False

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.hard_drop()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            pressing_down = False

    screen.fill(WHITE)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > -1:
                pygame.draw.rect(screen, colors[game.field[i][j]], [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for block in game.figure.image():
            i = block//4
            j = block%4
            pygame.draw.rect(screen, game.figure.color,
                [game.x + game.zoom*(j+game.figure.x)+1,
                 game.y + game.zoom*(i+game.figure.y)+1,
                 game.zoom-2, game.zoom-2])

    text_font = pygame.font.SysFont('Calibri', 25, True, False)
    title_font = pygame.font.SysFont('Calibri', 65, True, False)

    text_score = text_font.render("Score: " + str(game.score), True, BLACK)
    text_game_over = title_font.render("GAME OVER", True, (255, 125, 0))
    text_reset = title_font.render("Press ESC", True, (255, 215, 0))

    screen.blit(text_score, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_reset, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
