import matplotlib.pyplot as plt
import numpy as np
import gym

def plotLearning(scores, game_batch, filename):

    x = [ game_batch*i for i in range(len(scores)) ]

    plt.plot(x, scores, color="C1")

    plt.xlabel("Episodes")
    plt.ylabel("Score")
    plt.title("Average score in tetris per episode of deep reinforcement learning")

    plt.savefig(filename)
