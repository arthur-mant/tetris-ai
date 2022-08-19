from keras.models import Sequential
from keras.layers import Conv2D, Dense, Flatten
from tensorflow.keras.optimizers import Adam
from collections import deque

import numpy as np
import random
import os
import generate_field

def build_neural_network(input_shape, action_size, nn_layers, lr):
    if len(nn_layers) < 1:
        print("neural network needs at least 1 layer")
        return None

    model = Sequential()
    model.add(Conv2D(nn_layers[0][0][0], nn_layers[0][0][1], input_shape=input_shape))
    print("Created 2D convolutional layer with ", nn_layers[0][0][0], " filters of size", nn_layers[0][0][1])

    for layer in nn_layers[0][1:]:
        x = layer[0]
        y = layer[1]
        model.add(Conv2D(x, y))
        print("Created 2D convolutional layer with ", x, " filters of size", y)

    model.add(Flatten())
    for layer in nn_layers[1]:
        model.add(Dense(layer, activation='relu'))
        print("Created hidden dense layer with ", layer, " neurons")
    model.add(Dense(action_size, activation="linear"))
    model.compile(loss="mse", optimizer=Adam(learning_rate=lr))

    return model


class Agent():

    def __init__(self, input_shape, action_size, nn_layers, lr,
                    exploration_rate, exploration_min, exploration_decay,
                    gamma, sample_batch_size, new, init_size):

        self.input_shape = input_shape
        self.action_size = action_size
        self.nn_layers = nn_layers
        self.lr = lr
        self.exploration_rate = exploration_rate
        self.exploration_min = exploration_min
        self.exploration_decay = exploration_decay
        self.gamma = gamma
        self.sample_batch_size = sample_batch_size
        self.name = "agent"
        self.weight_backup_file = self.name+".h5"
        self.graph_name = self.name+".png"

        self.aux_nn_name = self.name+".precon"
        self.precon_backup_file = self.aux_nn_name+".h5"

        length = 10000
        self.memory = deque(maxlen=length)

        self.brain = build_neural_network(self.input_shape, self.action_size, self.nn_layers, self.lr)

        self.aux_brain = build_neural_network(self.input_shape, self.action_size, self.nn_layers, self.lr)

        if new:
            print("generating new neural network")
            field_v, action_v = generate_field.generate_experience_db(10, 20, init_size)
            print("finished generating basic experience")
            self.aux_brain.fit(
                np.reshape(field_v, [len(field_v)]+self.input_shape),
                np.reshape(action_v, [len(field_v), self.action_size]),
                epochs=100, verbose=0
            )
            print("finished basic training for new neural network")

        else:
            print("loading ", self.weight_backup_file, " neural network")
            if os.path.isfile(self.weight_backup_file):
                self.brain.load_weights(self.weight_backup_file)
            else:
                print("ERROR: ", self.weight_backup_file, " not found")

            print("loading ", self.precon_backup_file, " neural network")
            if os.path.isfile(self.precon_backup_file):
                self.aux_brain.load_weights(self.precon_backup_file)
            else:
                print("ERROR: ", self.precon_backup_file, " not found")


    def save_neural_network(self):
        print("saving neural network to ", self.weight_backup_file)
        self.brain.save(self.weight_backup_file)

    def act(self, state):
        possible_fields = utils.generate_all_fields(state)

        if np.random.rand() <= self.exploration_rate:
            min_dist = self.aux_brain.predict(possible_fields)[0]
            for field in possible_fields:
                distance = self.aux_brain.predict(field)[0]
                if min_dist > distance:
                    min_dist = dist
                    action = possible_fields.index(field)
        #act_values = self.brain.predict(state)[0]
        #return np.argmax(act_values)

        else:
            max_score = 0
            for field in possible_fields:
                score = self.brain.predict(field)[0]
                if max_score < score:
                    max_score = score
                    action = possible_fields.index(field)

        if len(possible_fields) <= 10:
            action = 2*action
        if len(possible_fields) <= 20:
            action = 2*action

        return action

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
