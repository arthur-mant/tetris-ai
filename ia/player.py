import sys
sys.path.insert(0, '/home/martinelli/tetris-ia/tetris')
import tetris
import game_controller
import generate_field
import heuristics

class Player:

    weights = []
    width = 0
    height = 0
    game_run = None
    controller = None

    def __init__(self, weights, width, height, fps=60):
        if len(weights) < 0:
            raise Exception("Invalid weight vector")
        if width < 4 or height < 4:
            raise Exception("Invalid field size")
        if fps < 0:
            raise Exception("Invalid FPS rate")
        self.weights = weights
        self.width = width
        self.height = height
        self.game_run = tetris.GameRun(
            tetris.Tetris(self.height, self.width, field=generate_field.generate_test_field(self.width, self.height)),
            fps
        )
        self.controller = game_controller.Controller(self.game_run)

    def exhaustive_search(self):
        all_pos = self.controller.get_all_possible_pos(self.game_run.game.field, self.game_run.game.piece.type)
        best_pos = all_pos[0]

        new_field, lines_cleared = self.controller.simulate_piece(best_pos, self.game_run.game.field, self.game_run.game.piece.type)
        score_best = heuristics.score(new_field, [lines_cleared], weights)

        for pos in all_pos:
            new_field, lines_cleared = self.controller.simulate_piece(pos, self.game_run.game.field, self.game_run.game.piece.type)
            all_next_pos = self.controller.get_all_possible_pos(new_field, self.game_run.game.next_piece.type)
            for next_pos in all_next_pos:
                #print(self.game_run.game.next_piece.type, next_pos)
                #for i in new_field:
                #    print(i)
                next_new_field, next_lines_cleared = self.controller.simulate_piece(next_pos, new_field, self.game_run.game.next_piece.type)
                score = heuristics.score(next_new_field, [lines_cleared, next_lines_cleared], weights)
                if score_best < score:
                    best_pos = pos
                    score_best = score
                #print("pos: ", pos, " next_pos", next_pos, " score: ", score)

        return best_pos, score_best

    def play(self):

        old_piece = -1
        new_field = None

        while self.game_run.run_frame() and self.game_run.game.state != "gameover":
            #triggers for every new piece
            if old_piece != self.game_run.game.pieces:

                #checks if previous piece was put where it was predicted
                self.controller.check_if_right_position(new_field)

                best_pos, best_score = self.exhaustive_search()
                #print("best position: ", best_pos, " score: ", best_score)

                #creates ideal field to compare with the actual field when the piece is placed
                new_field, _cleared_lines = self.controller.simulate_piece(best_pos, self.game_run.game.field, self.game_run.game.piece.type)
                #for i in new_field:
                #    print(i)

                #_unused = input()       #trava para executar uma peça por vez

                #sends command to put piece in the calculated place
                self.controller.put_piece(best_pos[2], best_pos[0], best_pos[1], path=best_pos[3])


            old_piece = self.game_run.game.pieces

        #print("Score: ", self.game_run.game.score)

        while self.game_run.run_frame():        #trava para ver o campo no gameover
            pass

        return self.game_run.game.score

if __name__ == '__main__':

    weights = [-10, -5, -5, 10, 10, -1000]
    player = Player(weights, 10, 20)
    player.play()
