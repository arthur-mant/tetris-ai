import sys
sys.path.insert(0, '/home/martinelli/tetris-ia/tetris')
import tetris
import game_controller
import generate_field

if __name__ == '__main__':

    width = 10
    height = 10

    game_run = tetris.GameRun(
        tetris.Tetris(height, width), #, field=generate_field.generate_plain_field(width, height, height//3, 3)),
        60
    )
    controller = game_controller.Controller(game_run.game)

    old_piece = -1

    while game_run.run_frame():
        if old_piece != game_run.game.pieces:
            print(controller.get_all_possible_pos())
        old_piece = game_run.game.pieces

    print("Score: ", game_run.game.score)
