import sys
sys.path.insert(0, '/home/martinelli/tetris-ia/tetris')
import tetris
import agent
import utils

import numpy as np

class AgentRun:
    def __init__(self, max_episodes, min_score, nn_layers, lr,
                    init_exp, exp_min, exp_decay, gamma, batch_size):

        self.max_episodes = max_episodes
        self.min_score = min_score
        self.scores = []

        self.agent = agent.Agent(214, 4, nn_layers, lr, init_exp, exp_min, exp_decay, gamma, batch_size)

    def run(self):
        index_episode = 0
        avg_score = 0
        eps_history = []

        #print("running agent")

        try:
            while index_episode < self.max_episodes and avg_score < self.min_score:

                #print("setting up game")
                tetris_run = tetris.GameRun(tetris.Tetris(20, 10), 600, use_screen=True, use_keyboard=False)
                state = utils.get_state(tetris_run.game)
                done = False

                while not done:
                    old_piece_count = tetris_run.game.pieces
                    #print("solving game")
                    prev_score = tetris_run.game.score
                    action = utils.num_to_action(tetris_run.game, self.agent.act(state))
                    tetris_run.run_frame(action)
                    reward = tetris_run.game.score - prev_score
                    next_state = utils.get_state(tetris_run.game)
                    done = tetris_run.game.gameover

                    #garante q quando uma peça for colocada o estado anterior
                    #não saberá qual é a próxima peça

                    remember_state = \
                        next_state \
                        if old_piece_count == tetris_run.game.pieces \
                        else next_state[:-7]+[0,0,0,0,0,0,0]

                    #print("state:\n", state, "\nnext_state:\n", next_state)
                    #print("altered next_state:\n", remember_state)

                    self.agent.remember(state, action, reward, remember_state, done)
                    state = next_state

                self.scores.append(tetris_run.game.score)
                eps_history.append(self.agent.exploration_rate)

                avg_score = np.mean(self.scores[max(0, index_episode-50):index_episode+1])
                print("Episode {} #Pieces: {} #Score: {} #Avg_Score: {} #Epsilon".format(
                    index_episode, tetris_run.game.pieces, tetris_run.game.score, avg_score, self.agent.exploration_rate))
                self.agent.replay()

                index_episode += 1
                tetris_run.close_game()
            print("finished running agent")

        finally:
            self.agent.save_neural_network()


