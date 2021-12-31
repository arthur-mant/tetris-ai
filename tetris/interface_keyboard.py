class Keyboard:
    def get_event_from_keyboard(self, pygame, game, pressing_down):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, False
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
                if event.key == pygame.K_ESCAPE and game.state == "gameover":
                    return True, False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False
        return False, pressing_down
