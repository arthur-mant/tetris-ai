import run_agent
import sys

if __name__ == '__main__':

    new = False
    if "--new" in sys.argv or "-n" in sys.argv:
        new = True

    use_screen = False
    if "--screen" in sys.argv or "-s" in sys.argv:
        use_screen = True

    init_exp = 1
    exp_min = 0.1
    if "-e" in sys.argv:
        try:
            init_exp = float(sys.argv[sys.argv.index("-e")+1])
        except:
            print("ERROR: unable to find initial epsilon USING DEFAULT VALUE 1")
        if init_exp < exp_min:
            exp_min = init_exp


    if "-d" in sys.argv or "--demo" in sys.argv:
        init_exp = 0
        exp_min = 0
        use_screen = True

    run_agent = \
        run_agent.AgentRun(
            max_episodes = 100000,
            min_score = 10000,
            nn_layers = [[(7, 3)], [100]],
            lr = 0.00001,
            init_exp = init_exp,
            exp_min = exp_min,
            exp_decay = 1,
            #exp_decay = 0.999,
            gamma = 0.99,
            game_batch = 50,
            init_size = 1000,
            new = new,
            use_screen = use_screen
        )
    run_agent.run()

