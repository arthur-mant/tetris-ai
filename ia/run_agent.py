import agent
import utils
import tetris

import numpy as np

class AgentRun:
    def __init__(self, max_episodes, min_score):
        self.max_episodes = max_episodes
        self.min_score = min_score
        self.scores = []

    def run(self):
        index_episode = 0
        avg_score = 0

        while index_episode < self.max_episodes and avg_score < min_score:
            try:
                tetris_run = tetris.GameRun(tetris.Tetris(20, 10), 60, use_screen=True, use_keyboard=False)
                state = utils.get_state(tetris_run.game)
                done = False
    
                while not done:
                    prev_score = tetris_run.game.score
                    action = utils.num_to_action(tetris_run.game, self.agent.act(state))
                    reward = tetris_run.game.score - prev_score
                    next_state = utils.get_state(tetris_run.game)
                    done = tetris_run.game.gameover
    
                    self.agent.remember(state, action, reward, next_state, done)
    
    
                self.scores.append(tetris_run.game.score)
                avg_score = np.mean(self.scores[max(0, index_episode-50):index_episode+1])
                print("Episode {} #Pieces: {} #Score: {} #Avg_Score: {}".format(
                    index_episode, tetris_run.game.pieces, tetris_run.game.score, avg_score)
                self.agent.replay()
    
                index_episode += 1
                tetris_run.close_game()
        finally:
            self.agent.save_neural_network()


