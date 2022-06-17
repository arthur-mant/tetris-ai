import sys
sys.path.insert(0, '/home/martinelli/tetris-ia/tetris')
import tetris
import agent
import utils
from collections import deque

import numpy as np

class AgentRun:
    def __init__(self, max_episodes, min_score, nn_layers, lr,
                    init_exp, exp_min, exp_decay, gamma, batch_size, new, use_screen):

        self.max_episodes = max_episodes
        self.min_score = min_score
        self.scores = []
        self.input_size = 248
        self.action_size = 40
        self.use_screen = use_screen


        self.agent = agent.Agent(self.input_size, 40, nn_layers, lr, init_exp, exp_min, exp_decay, gamma, batch_size, new)

    def run(self):
        index_episode = 0
        avg_score = 0
        eps_history = []

        #print("running agent")

        try:
            while index_episode < self.max_episodes and avg_score < self.min_score:

                #print("setting up game")
                tetris_run = tetris.GameRun(tetris.Tetris(20, 10), -1, use_screen=self.use_screen, use_keyboard=False)

                state = np.reshape(utils.get_state(tetris_run.game), [1, self.input_size])
                done = False

                while not done:

                    action = self.agent.act(state)
                    #print("action: ", action)

                    reward = tetris_run.step(action)
                    next_state = utils.get_state(tetris_run.game)

                    done = tetris_run.game.gameover

                    next_state = np.reshape(next_state, [1, self.input_size])

                    self.agent.remember(state, action, reward, next_state, done)

                    state = next_state

                self.scores.append(tetris_run.game.score)
                eps_history.append(self.agent.exploration_rate)

                avg_score = np.mean(self.scores[max(0, index_episode-50):index_episode+1])
                print("Episode {} #Pieces: {} #Score: {} #Avg_Score: {} #Epsilon {}".format(
                    index_episode, tetris_run.game.pieces, tetris_run.game.score, avg_score, self.agent.exploration_rate))
                self.agent.replay()

                index_episode += 1
                tetris_run.close_game()

                if index_episode % 5 == 0:
                    self.agent.save_neural_network()

            print("finished running agent")

        finally:
            self.agent.save_neural_network()


