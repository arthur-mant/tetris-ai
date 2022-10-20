from keras.models import Model
from keras.layers import Conv2D, Dense, Flatten, Input, Concatenate
from tensorflow.keras.optimizers import Adam
from collections import deque

import numpy as np
import random
import os
import generate_field

def build_neural_network(table_shape, action_size, nn_layers, lr):
    if len(nn_layers) < 1:
        print("neural network needs at least 1 layer")
        return None

    table_input = Input(shape=table_shape)

    for (i, layer) in enumerate(nn_layers[0]):

        if i == 0:
            conv = table_input

        x = layer[0]
        y = layer[1]
        conv = Conv2D(x, y, activation="relu")(conv)

        print("Created 2D convolutional layer with ", x, " filters of size", y)

    conv = Flatten()(conv)

    piece_input = Input(shape=[2*(7-1)])    #considera as 2 peças
                                            #retira 1 linha para ser LI
    concat = Concatenate()([conv, piece_input])

    for (i, layer) in enumerate(nn_layers[1]):

        if i == 0:
            hidden = concat

        hidden = Dense(layer, activation='relu')(hidden)
        print("Created hidden dense layer with ", layer, " neurons")

    output = Dense(action_size, activation="linear")(hidden)

    model = Model(inputs=[table_input, piece_input], outputs=output)
    model.compile(loss="mse", optimizer=Adam(learning_rate=lr))

    return model


class Agent():

    def __init__(self, table_shape, input_shape, action_size, nn_layers, lr,
                    exploration_rate, exploration_min, exploration_decay,
                    gamma, sample_batch_size, new, init_size):

        self.table_shape = table_shape
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

        print("building DQN")
        self.brain = build_neural_network(self.table_shape, self.action_size, self.nn_layers, self.lr)

        print("building auxiliary network")
        self.aux_brain = build_neural_network(self.table_shape, self.action_size, self.nn_layers, self.lr)

        if new:
            print("training new neural network")
            input_v, piece_v, action_v = generate_field.generate_experience_db(10, 20, init_size)
            print("finished generating basic experience")
            print(len(input_v))

            self.aux_brain.fit(
                [np.reshape(input_v, [len(input_v)]+self.input_shape[0]),
                    np.reshape(piece_v, [len(piece_v)]+self.input_shape[1])],
                np.reshape(action_v, [len(input_v), self.action_size]),
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
        print("saving DQN neural network to ", self.weight_backup_file)
        self.brain.save(self.weight_backup_file)

        print("saving auxiliary neural network to ", self.precon_backup_file)
        self.aux_brain.save(self.precon_backup_file)

    def act(self, state, piece, piece_v):

        if np.random.rand() <= self.exploration_rate:
            possible_fields, valid = utils.generate_all_fields(state, piece, piece_v)

            min_dist = self.aux_brain.predict(possible_fields)[0]
            for i in range(len(possible_fields)):
                if valid[i]:
                    distance = self.aux_brain.predict(possible_fields[i])[0]
                    if min_dist > distance:
                        min_dist = dist
                        action = i
            if len(possible_fields) <= 10:
                action = 2*action
            if len(possible_fields) <= 20:
                action = 2*action
            return action

        else:
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
