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
        self.use_screen = use_screen

        self.agent = agent.Agent(self.input_size, 4, nn_layers, lr, init_exp, exp_min, exp_decay, gamma, batch_size, new)

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
                state_history = deque(maxlen=20)

                while not done:
                    old_piece_count = tetris_run.game.pieces
                    #print("solving game")
                    prev_score = tetris_run.game.score
                    action = self.agent.act(state)

                    tetris_run.run_frame(utils.num_to_action(tetris_run.game, action))
                    next_state = utils.get_state(tetris_run.game)

                    #garante q quando uma peça for colocada o estado anterior
                    #não saberá qual é a próxima peça

                    remember_state = \
                        next_state \
                        if old_piece_count == tetris_run.game.pieces \
                        else next_state[:-7]+[0,0,0,0,0,0,0]


                    next_state = np.reshape(next_state, [1, self.input_size])
                    done = tetris_run.game.gameover

                    reward = (tetris_run.game.score - prev_score)*100

                    #adiciona um pequeno bonus se a peça se mover para baixo
                    if action == 1:
                        reward += 1
                    #adiciona penalidade pra rotações pra evitar bumerangue
                    if action == 0:
                        reward -= 1

                    #penalidade para ações q n fazem nada
                    if np.array_equal(state[0][200:], next_state[0][200:]) and \
                        old_piece_count == tetris_run.game.pieces:
                        reward -= 10000

                    #print(next_state[0][200:])
                    #print(list(state_history)[:10])

                    if len(state_history) == 20 and \
                        old_piece_count == tetris_run.game.pieces and \
                        next_state[0][200:] in list(state_history)[:10]:
                            print("stuck in the same moves")
                            done = True
                    state_history.append(next_state)
                    #calcula o numero de espaços preenchidos nas linhas afetadas pelo posicionamento da ultima peça

                    if old_piece_count != tetris_run.game.pieces:
                        index_list = [x for x in range(200) if (next_state[0][0:200] - state[0][0:200])[x] == 1]
                        index_list = list(dict.fromkeys([x//10 for x in index_list]))
                        for i in index_list:
                            non_holes = 0
                            for j in next_state[i*10:(i+1)*10]:
                                non_holes += 1

                        reward += 10*((len(index_list)*10 - non_holes)/(len(index_list)))


                    remember_state = np.reshape(remember_state, [1, self.input_size])

                    #print("state:\n", state, "\nnext_state:\n", next_state)
                    #print("altered next_state:\n", remember_state[0])
                    #print(reward)

                    self.agent.remember(state, action, reward, remember_state, done)
                    #state = np.reshape(next_state, [1, self.input_size])
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


