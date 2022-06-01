from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from collections import deque

import numpy as np
import random
#import os


def build_neural_network(input_dim, action_size, nn_layers, lr, filename):
    if len(nn_layers) < 1:
        print("neural network needs at least 1 layer")
        return None

    model = Sequential()
    model.add(Dense(nn_layers[0], input_dim=input_dim, activation="relu"))

    for layer in nn_layers[1:]:
        model.add(Dense(layer, activation="relu"))

    model.add(Dense(action_size, activation="linear"))
    model.compile(loss="mse", optimizer=Adam(learning_rate=lr))

#    if os.path.isfile(filename):
#        model.load_weights(filename)

    return model


class Agent():

    def __init__(self, input_dim, action_size, nn_layers, lr,
                    exploration_rate, exploration_min, exploration_decay,
                    gamma, sample_batch_size):

        self.input_dim = input_dim
        self.action_size = action_size
        self.nn_layers = nn_layers
        self.lr = lr
        self.exploration_rate = exploration_rate
        self.exploration_min = exploration_min
        self.exploration_decay = exploration_decay
        self.gamma = gamma
        self.sample_batch_size = sample_batch_size
        self.name = "TBD"
        self.weight_backup_file = self.name+".h5"

        self.brain = build_neural_network(self.input_dim, self.action_size, self.nn_layers, self.lr, self.weight_backup_file)

        self.memory = deque(maxlen=10000)


    def save_neural_network(self):
        self.brain.save(self.weight_backup_file)

    def act(self, state):
        if np.random.rand() <= self.exploration_rate:
            return random.randrange(self.action_size)
        act_values = self.brain(state)
        return np.argmax(act_values)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self):
        if len(self.memory) < self.sample_batch_size:
            return
        sample_batch = random.sample(self.memory, self.sample_batch_size)

        for state, action, reward, next_state, done in sample_batch:

            #print("state:\n", state, "next_state:\n", next_state)

            target = reward + self.gamma*int(not done)*np.amax(self.brain(next_state))
            target_f = self.brain(state)
            target_f[action] = target

            self.brain.fit(state, target_f, epochs=1, verbose=0)

        if self.exploration_rate > self.exploration_min:
            self.exploration_rate *= self.exploration_decay
