import run_agent
import sys

if __name__ == '__main__':


    init_epochs = 500
    if "-ie" in sys.argv:
        try:
            init_epochs = int(sys.argv[sys.argv.index("-ie")+1])
            print("init_epochs = ", init_epochs)
        except:
            print("ERROR: unable to find init epochs number USING DEFAULT VALUE ", init_epochs)

    epochs_per_batch = 50
    if "-eb" in sys.argv:
        try:
            epochs_per_batch = int(sys.argv[sys.argv.index("-eb")+1])
            print("epochs_per_batch = ", epochs_per_batch)
        except:
            print("ERROR: unable to find epochs per batch number USING DEFAULT VALUE", epochs_per_batch)

    game_batch = 100
    if "-gb" in sys.argv:
        try:
            game_batch = int(sys.argv[sys.argv.index("-gb")+1])
            print("game_batch = ", game_batch)
        except:
            print("ERROR: unable to find game batch number USING DEFAULT VALUE", game_batch)

    lr = 0.000000005
    if "-lr" in sys.argv:
        try:
            lr = float(sys.argv[sys.argv.index("-lr")+1])
            print("lr = ", lr)
        except:
            print("ERROR: unable to find learning rate number USING DEFAULT VALUE", lr)


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

    pretrain_only = False
    if "--pretrain" in sys.argv or "-pt" in sys.argv:
        pretrain_only = True
        name = "pretrained_only"
        new = True

    name = "default"
    if "--name" in sys.argv:
        try:
            name = str(sys.argv[sys.argv.index("--name")+1])
            print("name = ", name)
        except:
            print("ERROR: unable to find name USING DEFAULT VALUE ", name)

    run_agent = \
        run_agent.AgentRun(
            max_episodes = 100000,
            min_score = 100000,
            nn_layers = [[(20, 3)], [144]],
            lr = lr,                                #!!!
            gamma = 0.99,
            game_batch = game_batch,                #!!
            epochs_per_batch = epochs_per_batch,    #!!!
            new = new,
            init_epochs = init_epochs,              #!!!
            init_size = 50000,                     #qto mais, melhor
            init_batch = 10,
            depth = 3,
            use_screen = use_screen,
            sleep = sleep,
            name = name
        )
    if not pretrain_only:
        run_agent.run()

