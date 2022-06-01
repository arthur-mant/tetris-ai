import run_agent

if __name__ == '__main__':

    run_agent = \
        run_agent.AgentRun(
            max_episodes = 500,
            min_score = 1000,
            nn_layers = [64, 16],
            lr = 0.001,
            init_exp = 1,
            exp_min = 0.01,
            exp_decay = 0.99,
            gamma = 0.99,
            batch_size = 256
        )

