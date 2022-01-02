import sys
sys.path.insert(0, '/home/martinelli/tetris-ia/tetris')
import tetris
import game_controller
import generate_field
import heuristics

if __name__ == '__main__':

    width = 10
    height = 10

    game_run = tetris.GameRun(
        tetris.Tetris(height, width), #, field=generate_field.generate_plain_field(width, height, height//3, 3)),
        60
    )
    controller = game_controller.Controller(game_run)

    old_piece = -1
    weights = [-1, -1, -1]

    while game_run.run_frame() and game_run.game.state != "gameover":
        if old_piece != game_run.game.pieces:
            pos = controller.get_all_possible_pos()
            #print(pos)
            best_pos = pos[0]
            aux = heuristics.score(controller.simulate_piece(best_pos[0], best_pos[1], best_pos[2]), weights)

            for elem in pos:
                aux2=heuristics.score(controller.simulate_piece(elem[0], elem[1], elem[2]), weights)
                if aux < aux2:
                    best_pos = elem
                    aux = aux2
                print("element: ", elem, "score: ", aux2)
            print("best position: ", best_pos)
            _unused = input()
            controller.put_piece(best_pos[2], best_pos[0], best_pos[1], path=best_pos[3])
        old_piece = game_run.game.pieces

    print("Score: ", game_run.game.score)

    while game_run.run_frame():
        pass
