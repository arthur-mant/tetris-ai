from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from collections import deque

import numpy as np
import random
import os


def build_neural_network(input_dim, nn_layers, lr, filename):
    if len(nn_layers) < 1:
        print("neural network needs at least 1 layer")
        return None

    print("input dim ", input_dim)

    model = Sequential()
    model.add(Dense(nn_layers[0], input_dim=input_dim, activation="relu"))

    for layer in nn_layers[1:]:
        model.add(Dense(layer, activation="relu"))

    model.add(Dense(1, activation="linear"))
    model.compile(loss="mse", optimizer=Adam(learning_rate=lr))

#    if os.path.isfile(filename):
#        model.load_weights(filename)

    return model


class Agent():

    def __init__(self, input_dim, nn_layers, lr,
                    exploration_rate, exploration_min, exploration_decay,
                    gamma, sample_batch_size, new):

        self.input_dim = input_dim
        self.nn_layers = nn_layers
        self.lr = lr
        self.exploration_rate = exploration_rate
        self.exploration_min = exploration_min
        self.exploration_decay = exploration_decay
        self.gamma = gamma
        self.sample_batch_size = sample_batch_size
        self.name = "TBD"
        self.weight_backup_file = self.name+".h5"
        self.memory = deque(maxlen=10000)


        self.brain = build_neural_network(self.input_dim, self.nn_layers, self.lr, self.weight_backup_file)

        if new:
            print("generating new neural network")
        else:
            print("loading ", self.weight_backup_file, " neural network")
            if os.path.isfile(self.weight_backup_file):
                self.brain.load_weights(self.weight_backup_file)
            else:
                print("ERROR: ", self.weight_backup_file, " not found")



    def save_neural_network(self):
        print("saving neural network to ", self.weight_backup_file)
        self.brain.save(self.weight_backup_file)

    def act(self, game):
        if np.random.rand() <= self.exploration_rate:
            return (random.randrange(game.width)-1, \
                    -2, \
                    random.randrange(len(game.piece.pieces[game.piece.type]))
        pos_states = utils.get_all_states(game)
        pos_fields = []
        field_scores = []

        max_score = None
        index_max = -1

        for i in range(pos_states):

            aux = self.brain.predict(utils.get_state(game, utils.coordinates_to_field(game, pos_states[i])))[0]

            if max_score == None or aux > max_score:
                max_score = aux
                index_max = i

        return pos_states[index_max]

    def remember(self, state, reward, next_state, done):
        self.memory.append((state, reward, next_state, done))

    def replay(self):
        if len(self.memory) < self.sample_batch_size:
            return
        sample_batch = random.sample(self.memory, self.sample_batch_size)

        for state, reward, next_state, done in sample_batch:

            target = reward + self.gamma*int(not done)*np.amax(self.brain.predict(next_state)[0])
            target_f = self.brain.predict(state)
            target_f[0][0] = target

            self.brain.fit(state, target_f, epochs=1, verbose=0)

        if self.exploration_rate > self.exploration_min:
            self.exploration_rate *= self.exploration_decay
        else:
            self.exploration_rate = self.exploration_min
