from keras.models import Model
from keras.layers import Conv2D, Dense, Flatten, Input, Concatenate
from tensorflow.keras.optimizers import Adam
from collections import deque
from tetris import Tetris

import numpy as np
import random
import os
import generate_field
import time

import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
#tf.debugging.set_log_device_placement(True) # mostra logs do que usa gpu


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

    piece_input = Input(shape=[(7-1)])      #considera a prox peça
                                            #retira 1 linha para ser LI
    concat = Concatenate()([conv, piece_input])

    for (i, layer) in enumerate(nn_layers[1]):

        if i == 0:
            hidden = concat

        hidden = Dense(layer, activation='relu')(hidden)
        print("Created hidden dense layer with ", layer, " neurons")

    output = Dense(action_size, activation="linear")(hidden)

    model = Model(inputs=[table_input, piece_input], outputs=output)
    model.compile(
                    loss="mse",
                    optimizer=Adam(learning_rate=lr)
                )

    return model


class Agent():

    def __init__(self, table_shape, input_shape, action_size, nn_layers, lr,
                    gamma, game_batch, epochs_per_batch, new, init_epochs,
                    init_size, init_batch, depth, name):

        self.table_shape = table_shape
        self.input_shape = input_shape
        self.action_size = action_size
        self.nn_layers = nn_layers
        self.lr = lr
        self.gamma = gamma
        self.game_batch = game_batch
        self.epochs_per_batch = epochs_per_batch
        self.name = name
        self.directory = "./resultados/"+self.name+"/"
        self.weight_backup_file = self.directory+"nn.h5"
        self.graph_name = self.directory+self.name+".png"

        #length = 10000
        #self.memory = deque(maxlen=self.game_batch)
        self.memory = [ [] for i in range(self.game_batch) ]

        if os.path.exists(self.directory):
            print("WARNING: will override "+self.directory)
        else:
            os.makedirs(self.directory)

        print("building DQN")
        self.brain = build_neural_network(self.table_shape, self.action_size, self.nn_layers, self.lr)


        if not new:
            print("loading ", self.weight_backup_file, " neural network")
            if os.path.isfile(self.weight_backup_file):
                self.brain.load_weights(self.weight_backup_file)
            else:
                print("ERROR: ", self.weight_backup_file, " not found, generating new")
                new = True

        if new:
            print("training new neural network")

            for i in range(init_batch):
                input_v, piece_v, action_v = generate_field.generate_experience_db(10, 20, init_size, depth)
                print(i, " finished generating basic experience")

                begin_time = time.time()

                self.brain.fit(
                    [np.reshape(input_v, [len(input_v)]+self.input_shape[0]),
                        np.reshape(piece_v, [len(piece_v)]+self.input_shape[1])],
                    np.reshape(action_v, [len(input_v), self.action_size]),
                    epochs=init_epochs, verbose=0, shuffle=True
                )
                print(i, " took ", time.time()-begin_time, "s to train nn")
                print(i, " finished basic training for new neural network")
                self.save_neural_network(0)

    def save_neural_network(self, num=-1):
        if num >= 0:
            backup_file = self.weight_backup_file.replace(".h5", str(num)+".h5")
        else:
            backup_file = self.weight_backup_file
        print("saving DQN neural network to ", backup_file)
        self.brain.save(backup_file)

    def act(self, state):
        act_values = self.brain.predict(state)[0]
        return np.argmax(act_values)


    def remember(self, game_id, game_record, score):
        self.memory[(game_id % self.game_batch)-1] = (game_id, game_record, score)

    def replay(self):
        table_v = []
        piece_v = []
        out_v = []

        highest_score = 0

        segments = []

        for game_id, game_record, score in self.memory:

            highest_score = max(highest_score, score)

            aux_segment = {"segment_score": 0, "moves": [], "game_score": score}

            for move in game_record:

                aux_segment["moves"].append(move)

                segment_score = 0
                for line_score in Tetris.line_score:
                    if move[2] >= line_score:               #reward
                        segment_score = line_score
                if move[4]:                                 #done
                    segment_score = -1*Tetris.line_score[-1]

                if segment_score != 0:
                    aux_segment["segment_score"] = segment_score
                    segments.append(aux_segment)
                    aux_segment = {"segment_score": 0, "moves": [], "game_score": score}


        segments = sorted(segments, key=lambda d:
                        (pow(d["segment_score"], 3)/len(d["moves"]))
                    )

        #for segment in segments:
        #    print("  segment score: ", segment["segment_score"])
        #    print("  number of moves: ", len(segment["moves"]))

        for segment in segments[int(0.8*len(segments)):]:
            for state, action, reward, next_state, done in segment["moves"]:

                #individual
                #segmento
                #futuro
                #global

                target = \
                    (reward +\
                    pow(segment["segment_score"], 3)/(len(segment["moves"])*pow(Tetris.line_score[0], 2)) +\
                    self.gamma*int(not done)*np.amax(self.brain.predict(next_state)[0]))

                if target >= 0:
                    target *= (segment["game_score"]/highest_score)
                else:
                    target *= (1 - (segment["game_score"]/highest_score))


                target_f = self.brain.predict(state)
                target_f[0][action] = target

                table_v.append(state[0])
                piece_v.append(state[1])
                out_v.append(target_f)

        self.brain.fit(
                [np.reshape(table_v, [len(table_v)]+self.input_shape[0]),
                    np.reshape(piece_v, [len(piece_v)]+self.input_shape[1])],
                np.reshape(out_v, [len(out_v), self.action_size]),
            epochs=self.epochs_per_batch, verbose=0, shuffle=True)

    def evaluate_accuracy(self, test_data):
        nn_output = self.brain.predict(test_data["X"])

        hit = 0
        for i in range(len(nn_output)):
            if np.argmax(nn_output[i]) == np.argmax(test_data["Y"][i]):
                hit += 1

        return hit/len(nn_output)


