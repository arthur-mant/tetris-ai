import sys
sys.path.insert(0, './tetris')
import tetris
import agent
import utils
import time
import pickle
import numpy as np
from collections import deque
from graph import plotLearning

import numpy as np

class AgentRun:
    def __init__(self, max_episodes, min_score, nn_layers, lr, lr_pt,
                    gamma, game_batch, epochs_per_batch, new, init_epochs,
                    init_size, init_batch, depth, use_screen, sleep, config, pt_test):

        self.max_episodes = max_episodes
        self.min_score = min_score
        self.scores = []
        self.avg_scores = []
        self.accuracy = []
        self.eps_history = []
        self.table_shape = [20, 10, 1]
        self.input_shape = (self.table_shape, [(7-1)])
        self.output_size = 40
        self.use_screen = use_screen
        self.game_batch = game_batch

        try:
            with open("dataset.pickle", 'rb') as f:
                self.test_data = pickle.load(f)
        except IOError:
            sys.exit("file dataset.pickle not found. stopping execution")

        self.agent = agent.Agent(self.table_shape, self.input_shape, self.output_size, nn_layers, lr, lr_pt, gamma, self.game_batch, epochs_per_batch, new, init_epochs, init_size, init_batch, depth, config)

        if pt_test:
            self.log_filename = self.agent.pt_directory+"out.log"
        else:
            self.log_filename = self.agent.directory+"out.log"
        self.log_file = open(self.log_filename, 'w')
        self.sleep = sleep

    def run(self):
        index_episode = 1
        avg_score = 0

        aux_time = time.time()

        try:
            while index_episode < self.max_episodes and avg_score < self.min_score:

                tetris_run = tetris.GameRun(tetris.Tetris(20, 10), -1, use_screen=self.use_screen, use_keyboard=False)

                #state = np.reshape(utils.get_state(tetris_run.game), [1]+self.input_shape)
                state = utils.get_state(tetris_run.game, self.input_shape)
                game_record = []
                done = False

                while not done:

                    if self.use_screen and self.sleep > 0:
                        time.sleep(self.sleep)

                    action = self.agent.act(state)
                    reward = tetris_run.step(action)
                    next_state = utils.get_state(tetris_run.game, self.input_shape)
                    done = tetris_run.game.gameover


                    game_record.append((state, action, reward, next_state, done))

                    state = next_state

                self.agent.remember(index_episode, game_record, tetris_run.game.score)

                self.scores.append(tetris_run.game.score)

                avg_score = np.mean(self.scores[max(0, index_episode-500):])

                log_str = "Episode {} #Pieces: {} #Score: {} #Avg Score: {}".format(
                    index_episode, tetris_run.game.pieces, tetris_run.game.score, avg_score)

                print(log_str)
                self.log_file.write(log_str+"\n")

                index_episode += 1

                if (index_episode-1) % self.game_batch == 0:
                    self.avg_scores.append(avg_score)
                    self.accuracy.append(
                            self.agent.evaluate_accuracy(self.test_data)
                    )
                    print("Accuracy: ", self.accuracy[-1])

                    print("time spent on games: ", time.time()-aux_time, " s")
                    aux_time = time.time()
                    self.agent.replay()
                    print("time spent on replay: ", time.time()-aux_time, " s")
                    aux_time = time.time()

                tetris_run.close_game()

                if (index_episode-1) % (10*self.game_batch) == 0:
                    print("Saving...")

                    aux_time = time.time()

                    plotLearning(self.avg_scores, self.accuracy, self.game_batch, self.agent.graph_name)

                    self.agent.save_neural_network()
                    self.agent.save_neural_network((index_episode-1) // (10*self.game_batch))
                    self.log_file.close()
                    self.log_file = open(self.log_filename, 'a')

                    print("saving took ", time.time()-aux_time, " s")
                    aux_time = time.time()

            print("finished running agent")

        finally:

            self.log_file.write(
                self.agent.evaluate_accuracy(self.test_data)
            )
            self.log_file.close()
            self.agent.save_neural_network()
            plotLearning(self.avg_scores, self.accuracy, self.game_batch, self.agent.graph_name)

