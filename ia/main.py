import run_agent
import sys

if __name__ == '__main__':

    new = False
    if "--new" in sys.argv or "-n" in sys.argv:
        new = True

    use_screen = False
    if "--screen" in sys.argv or "-s" in sys.argv:
        use_screen = True

    sleep = -1
    if "-d" in sys.argv or "--demo" in sys.argv:
        sleep = 0.5
        use_screen = True

    run_agent = \
        run_agent.AgentRun(
            max_episodes = 100000,
            min_score = 10000,
            nn_layers = [[(7, 3)], [100]],
            lr = 0.00001,
            gamma = 0.99,
            game_batch = 100,
            epochs_per_batch = 100,
            new = new,
            init_epochs = 200,
            init_size = 100000,
            use_screen = use_screen,
            sleep = sleep
        )
    run_agent.run()

