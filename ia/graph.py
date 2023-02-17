import matplotlib.pyplot as plt
import numpy as np
import gym

def plotLearning(avg_lines, accuracy, batch_size, filename):

    x = [ batch_size*(i+1) for i in range(len(avg_lines[0])) ]

    fig = plt.figure()

    ax = fig.add_subplot(111, label="1")
    ax2 = fig.add_subplot(111, label="2", frame_on=False)

    ax.plot(x, accuracy, color="C0")
    ax.set_xlabel("Episódio", color="C0")
    ax.set_ylabel("Métrica m", color="C0")
    ax.tick_params(axis='x', colors="C0")
    ax.tick_params(axis='y', colors="C0")

    ax2.plot(x, avg_lines[0], color="C1", label='1')
    ax2.plot(x, avg_lines[1], color="C2", label='2')
    ax2.plot(x, avg_lines[2], color="C3", label='3')
    ax2.plot(x, avg_lines[3], color="C5", label='4')
    ax2.legend()
    ax2.axes.get_xaxis().set_visible(False)
    ax2.yaxis.tick_right()
    ax2.set_ylabel("Média de linhas fechadas simultaneamente", color="C1")
    ax2.yaxis.set_label_position('right')
    ax2.tick_params(axis='y', colors="C1")

    plt.title("Tetris usando aprendizado por reforço")

    plt.savefig(filename)
