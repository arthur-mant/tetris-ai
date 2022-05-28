from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from collections import deque

#import os


def build_neural_network(self, input_dim, action_size, nn_layers, lr, filename):
    if len(nn_layers) < 1:
        print("neural network needs at least 1 layer")
        return None

    model = Sequential()
    model.add(Dense(nn_layers[0], input_dim=input_dim, activation="relu")

    for layer in nn_layers[1:]:
        model.add(Dense(layer, activation="relu"))

    model.add(Dense(action_size, activation="linear"))
    model.compile(loss="mse", optimizer=Adam(learning_rate=lr)

#    if os.path.isfile(filename):
#        model.load_weights(filename)

    return model


class Agent():

    def __init__(self, input_dim, action_size, nn_layers, lr):
        self.input_dim = input_dim
        self.action_size = action_size
        self.nn_layers = nn_layers
        self.lr = lr
        self.weight_backup_file = "TBD"

        self.brain = build_neural_network(self.input_dim, self.action_size, self.nn_layers, self.lr, self.weight_backup_file)

        self.memory = deque(maxlen=10000)


    def save_neural_network(self):
        self.brain.save(self.weight_backup_file)

    def act(self, state):

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))


