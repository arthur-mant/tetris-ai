import matplotlib.pyplot as plt
import numpy as np
import gym

def plotLearning(avg_scores, accuracy, batch_size, filename):

    x = [ batch_size*(i+1) for i in range(len(avg_scores)) ]

    fig = plt.figure()

    ax = fig.add_subplot(111, label="1")
    ax2 = fig.add_subplot(111, label="2", frame_on=False)

    ax.plot(x, accuracy, color="C0")
    ax.set_xlabel("Episode", color="C0")
    ax.set_ylabel("Accuracy", color="C0")
    ax.tick_params(axis='x', colors="C0")
    ax.tick_params(axis='y', colors="C0")

    ax2.plot(x, avg_scores, color="C1")
    ax2.axes.get_xaxis().set_visible(False)
    ax2.yaxis.tick_right()
    ax2.set_ylabel("Score", color="C1")
    ax2.yaxis.set_label_position('right')
    ax2.tick_params(axis='y', colors="C1")

    plt.title("Tetris using deep reinforcement learning")

    plt.savefig(filename)
