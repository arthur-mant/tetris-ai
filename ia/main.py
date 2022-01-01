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
            pos = controller.get_all_possible_pos()
            print(pos)
            best_pos = pos[0]
            for elem in pos:
                if best_pos[1] < elem[1]:
                    best_pos = elem
            print("best position: ", best_pos)
            controller.put_piece(best_pos[2], best_pos[0], best_pos[1], path=best_pos[3])
        old_piece = game_run.game.pieces

    print("Score: ", game_run.game.score)
