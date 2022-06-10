import run_agent
import sys

if __name__ == '__main__':

    new = False
    if "--new" in sys.argv:
        new = True

    use_screen = False
    if "--screen" in sys.argv:
        use_screen = True

    init_exp = 1
    if "-e" in sys.argv:
        try:
            init_exp = float(sys.argv[sys.argv.index("-e")+1])
        except:
            print("ERROR: unable to find initial epsilon USING DEFAULT VALUE 1")

    run_agent = \
        run_agent.AgentRun(
            max_episodes = 10000,
            min_score = 10000,
            nn_layers = [64, 64],
            lr = 0.001,
            init_exp = init_exp,
            exp_min = 0.01,
            exp_decay = 0.99,
            gamma = 0.99,
            batch_size = 256,
            new = new,
            use_screen = use_screen
        )
    run_agent.run()

