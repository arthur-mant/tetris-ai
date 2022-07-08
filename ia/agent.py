from keras.models import Sequential
from keras.layers import Conv2D, Dense, Flatten
from tensorflow.keras.optimizers import Adam
from collections import deque

import numpy as np
import random
import os


def build_neural_network(input_shape, action_size, nn_layers, lr, filename):
    if len(nn_layers) < 1:
        print("neural network needs at least 1 layer")
        return None

    model = Sequential()
    model.add(Conv2D(nn_layers[0][0], nn_layers[0][1], input_shape=input_shape))

    for layer in nn_layers[1:]:
        x = layer[0]
        y = layer[1]
        model.add(Conv2D(x, y))

    model.add(Flatten())
    model.add(Dense(action_size, activation="linear"))
    model.compile(loss="mse", optimizer=Adam(learning_rate=lr))

    return model


class Agent():

    def __init__(self, input_shape, action_size, nn_layers, lr,
                    exploration_rate, exploration_min, exploration_decay,
                    gamma, sample_batch_size, new):

        self.input_shape = input_shape
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
        self.graph_name = self.name+".png"

        self.memory = deque(maxlen=10000)


        self.brain = build_neural_network(self.input_shape, self.action_size, self.nn_layers, self.lr, self.weight_backup_file)

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

    def act(self, state):
        if np.random.rand() <= self.exploration_rate:
            return random.randrange(self.action_size)
        act_values = self.brain.predict(state)[0]
        return np.argmax(act_values)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self):
        if len(self.memory) < self.sample_batch_size:
            return
        sample_batch = random.sample(self.memory, self.sample_batch_size)

        for state, action, reward, next_state, done in sample_batch:

            target = reward + self.gamma*int(not done)*np.amax(self.brain.predict(next_state)[0])
            target_f = self.brain.predict(state)
            target_f[0][action] = target

            self.brain.fit(state, target_f, epochs=1, verbose=0)

        if self.exploration_rate > self.exploration_min:
            self.exploration_rate *= self.exploration_decay
        else:
            self.exploration_rate = self.exploration_min
