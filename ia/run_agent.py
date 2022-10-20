import sys
sys.path.insert(0, '/home/martinelli/tetris-ia/tetris')
import tetris
import agent
import utils
import time
import numpy as np
from collections import deque
from graph import plotLearning

import numpy as np

class AgentRun:
    def __init__(self, max_episodes, min_score, nn_layers, lr,
                    init_exp, exp_min, exp_decay, gamma, batch_size, game_batch, init_size, new, use_screen):

        self.max_episodes = max_episodes
        self.min_score = min_score
        self.scores = []
        self.avg_scores = []
        self.eps_history = []
        self.table_shape = [20, 10, 1]
        self.input_shape = (self.table_shape, [2*(7-1)])
        self.output_size = 40
        self.use_screen = use_screen
        self.game_batch = game_batch


        self.agent = agent.Agent(self.table_shape, self.input_shape, self.output_size, nn_layers, lr, init_exp, exp_min, exp_decay, gamma, batch_size, new, init_size)

    def run(self):
        index_episode = 1
        avg_score = 0

        aux_time = time.time()

        try:
            while index_episode < self.max_episodes and avg_score < self.min_score:

                tetris_run = tetris.GameRun(tetris.Tetris(20, 10), -1, use_screen=self.use_screen, use_keyboard=False)

                #state = np.reshape(utils.get_state(tetris_run.game), [1]+self.input_shape)
                state = utils.get_state(tetris_run.game, self.input_shape)
                done = False

                while not done:

                    action = self.agent.act(state)
                    reward = tetris_run.step(action)
                    #next_state = np.reshape(utils.get_state(tetris_run.game), [1]+self.input_shape)
                    next_state = utils.get_state(tetris_run.game, self.input_shape)
                    done = tetris_run.game.gameover


                    self.agent.remember(state, action, reward, next_state, done)

                    state = next_state

                self.scores.append(tetris_run.game.score)
                avg_score = np.mean(self.scores[max(0, index_episode-50):index_episode+1])
                self.avg_scores.append(avg_score)
                self.eps_history.append(self.agent.exploration_rate)


                print("Episode {} #Pieces: {} #Score: {} #Avg_Score: {} #Epsilon {}".format(
                    index_episode, tetris_run.game.pieces, tetris_run.game.score, avg_score, self.agent.exploration_rate))

                index_episode += 1

                if (index_episode-1) % self.game_batch == 0:
                    print("time spent on games: ", time.time()-aux_time, " s")
                    aux_time = time.time()
                    self.agent.replay()
                    print("time spent on replay: ", time.time()-aux_time, " s")
                    aux_time = time.time()

                tetris_run.close_game()

                if (index_episode-1) % (10*self.game_batch) == 0:
                    self.agent.save_neural_network()

            print("finished running agent")

        finally:
            self.agent.save_neural_network()

            x = [i+1 for i in range(index_episode-1)]
            plotLearning(x, self.scores, self.eps_history, self.agent.graph_name)

