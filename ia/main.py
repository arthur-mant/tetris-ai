import run_agent
import sys

if __name__ == '__main__':

    new = False
    if "--new" in sys.argv:
        new = True

    run_agent = \
        run_agent.AgentRun(
            max_episodes = 500,
            min_score = 1000,
            nn_layers = [64, 16],
            lr = 0.001,
            init_exp = 1,
            exp_min = 0.01,
            exp_decay = 0.95,
            gamma = 0.99,
            batch_size = 128,
            new = new
        )
    run_agent.run()

