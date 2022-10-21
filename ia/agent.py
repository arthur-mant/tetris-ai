from keras.models import Model
from keras.layers import Conv2D, Dense, Flatten, Input, Concatenate
from tensorflow.keras.optimizers import Adam
from collections import deque

import numpy as np
import random
import os
import generate_field
import time

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
                    gamma, game_batch, new, init_size):

        self.table_shape = table_shape
        self.input_shape = input_shape
        self.action_size = action_size
        self.nn_layers = nn_layers
        self.lr = lr
        self.exploration_rate = exploration_rate
        self.exploration_min = exploration_min
        self.exploration_decay = exploration_decay
        self.gamma = gamma
        self.game_batch = game_batch
        self.name = "agent"
        self.weight_backup_file = self.name+".h5"
        self.graph_name = self.name+".png"

        self.aux_nn_name = self.name+".precon"
        self.precon_backup_file = self.aux_nn_name+".h5"

        #length = 10000
        #self.memory = deque(maxlen=self.game_batch)
        self.memory = [ [] for i in range(self.game_batch) ]

        print("building DQN")
        self.brain = build_neural_network(self.table_shape, self.action_size, self.nn_layers, self.lr)

        print("building auxiliary network")
        self.aux_brain = build_neural_network(self.table_shape, self.action_size, self.nn_layers, self.lr)

        if new:
            print("training new neural network")
            input_v, piece_v, action_v = generate_field.generate_experience_db(10, 20, init_size)
            print("finished generating basic experience")

            begin_time = time.time()

            self.aux_brain.fit(
                [np.reshape(input_v, [len(input_v)]+self.input_shape[0]),
                    np.reshape(piece_v, [len(piece_v)]+self.input_shape[1])],
                np.reshape(action_v, [len(input_v), self.action_size]),
                epochs=200, verbose=0
            )
            print("took ", time.time()-begin_time, "s to train nn")
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

    def act(self, state):
        if np.random.rand() <= self.exploration_rate:
            brain_used = self.aux_brain
        else:
            brain_used = self.brain
        act_values = brain_used.predict(state)[0]
        return np.argmax(act_values)


    #def remember(self, state, action, reward, next_state, done):
    #    self.memory.append((state, action, reward, next_state, done))
    def remember(self, game_id, game_record, score):
        self.memory[(game_id % self.game_batch)-1] = (game_id, game_record, score)

    def replay(self):
        table_v = []
        piece_v = []
        out_v = []

        self.memory.sort(key=lambda y: y[2])    #ordena pelo score
        sample_batch = self.memory[:self.game_batch//10] + self.memory[9*self.game_batch//10:]

        for game_id, game_record, score in sample_batch:
            for state, action, reward, next_state, done in game_record:

                target = reward + self.gamma*int(not done)*np.amax(self.brain.predict(next_state)[0])
                target_f = self.brain.predict(state)
                target_f[0][action] = target

                table_v.append(state[0])
                piece_v.append(state[1])
                out_v.append(target_f)

        self.brain.fit(
                [np.reshape(table_v, [len(table_v)]+self.input_shape[0]),
                    np.reshape(piece_v, [len(piece_v)]+self.input_shape[1])],
                np.reshape(out_v, [len(out_v), self.action_size]),
            epochs=10, verbose=0)

        if self.exploration_rate > self.exploration_min:
            self.exploration_rate *= self.exploration_decay
        else:
            self.exploration_rate = self.exploration_min
