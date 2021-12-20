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
        self.color = colors[self.type]
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

    state = "start"
    x = 0
    y = 0
    zoom = 1
    piece = None
    next_piece = None

    def __init__(self, height, width, x, y, zoom):      #should be at least 4x4
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.zoom = zoom
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
                print("eliminate line")
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

    window_width = 400
    window_lenght = 500
    screen = pygame.display.set_mode((window_width, window_lenght))

    screen_width_margin = window_width/8

    pygame.display.set_caption("Tetris")

    done = False
    clock = pygame.time.Clock()
    fps = 60
    game = Tetris(20, 10, 100, 60, 20)
    counter = 0
    game_over = False

    pressing_down = False

    while not done:
        if game.piece is None:
            game.new_piece()
        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (fps // (2*game.level)) == 0 or pressing_down:
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
                if event.key == pygame.K_ESCAPE and game_over:
                    game.__init__(20, 10)
                    game_over = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

        screen.fill(WHITE)

        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                if game.field[i][j] > -1:
                    pygame.draw.rect(screen, colors[game.field[i][j]], [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

        if game.piece is not None:
            for block in game.piece.image():
                i = block//4
                j = block%4
                pygame.draw.rect(screen, game.piece.color,
                    [game.x + game.zoom*(j+game.piece.x)+1,
                     game.y + game.zoom*(i+game.piece.y)+1,
                     game.zoom-2, game.zoom-2])

        text_font = pygame.font.SysFont('Calibri', 25, True, False)
        title_font = pygame.font.SysFont('Calibri', 65, True, False)

        text_score = text_font.render("Score: " + str(game.score), True, BLACK)

        text_lines = text_font.render("Lines: " + str(game.lines), True, BLACK)
        text_pieces = text_font.render("Pieces: " + str(game.pieces), True, BLACK)
        text_level = text_font.render("Level: " + str(game.level), True, BLACK)

        text_game_over = title_font.render("GAME OVER", True, (255, 125, 0))
        text_reset = title_font.render("Press ESC", True, (255, 215, 0))

        screen.blit(text_score, [screen_width_margin, 0])
        screen.blit(text_lines, [window_width // 2 + screen_width_margin, 0])
        screen.blit(text_pieces, [screen_width_margin, 50])
        screen.blit(text_level, [window_width // 2 + screen_width_margin, 50])
        if game.state == "gameover":
            screen.blit(text_game_over, [20, 200])
            screen.blit(text_reset, [25, 265])
            game_over = True

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
