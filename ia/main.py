import run_agent
import sys

if __name__ == '__main__':

    name = "default"
    config = []
    if "--name" in sys.argv:
        try:
            name = str(sys.argv[sys.argv.index("--name")+1])
            print("name = ", name)
        except:
            print("ERROR: unable to find name USING DEFAULT VALUE ", name)


    init_epochs = 500
    if "-ie" in sys.argv:
        try:
            init_epochs = int(sys.argv[sys.argv.index("-ie")+1])
            print("init_epochs = ", init_epochs)
            config.append({"string":"IE"+str(init_epochs), "pretraining": True})
        except:
            print("ERROR: unable to find init epochs number USING DEFAULT VALUE ", init_epochs)

    epochs_per_batch = 50
    if "-eb" in sys.argv:
        try:
            epochs_per_batch = int(sys.argv[sys.argv.index("-eb")+1])
            print("epochs_per_batch = ", epochs_per_batch)
            config.append({"string":"EB"+str(epochs_per_batch), "pretraining": True})
        except:
            print("ERROR: unable to find epochs per batch number USING DEFAULT VALUE", epochs_per_batch)

    game_batch = 100
    if "-gb" in sys.argv:
        try:
            game_batch = int(sys.argv[sys.argv.index("-gb")+1])
            print("game_batch = ", game_batch)
            config.append({"string":"GB"+str(game_batch), "pretraining": False})
        except:
            print("ERROR: unable to find game batch number USING DEFAULT VALUE", game_batch)

    lr_pt = 0.00001
    if "-lrpt" in sys.argv:
        try:
            lr_pt = float(sys.argv[sys.argv.index("-lrpt")+1])
            print("lr_pt = ", lr_pt)
            config.append({"string":"LRPT"+str(lr_pt), "pretraining": True})
        except:
            print("ERROR: unable to find learning rate number USING DEFAULT VALUE", lr)

    lr = 0.00000001
    if "-lr" in sys.argv:
        try:
            lr = float(sys.argv[sys.argv.index("-lr")+1])
            print("lr = ", lr)
            config.append({"string":"LR"+str(lr), "pretraining": False})
        except:
            print("ERROR: unable to find learning rate number USING DEFAULT VALUE", lr)


    init_batch = 10
    if "-ib" in sys.argv:
        try:
            init_batch = int(sys.argv[sys.argv.index("-ib")+1])
            print("init_batch = ", init_batch)
            config.append({"string":"IB"+str(init_batch), "pretraining": True})
        except:
            print("ERROR: unable to find init batch number USING DEFAULT VALUE", init_batch)

    init_size = 100000
    if "-is" in sys.argv:
        try:
            init_size = int(sys.argv[sys.argv.index("-is")+1])
            print("init_size = ", init_size)
            config.append({"string":"IS"+str(init_size), "pretraining": True})
        except:
            print("ERROR: unable to find init size number USING DEFAULT VALUE", init_size)

    seg_frac = 0.2
    if "-sf" in sys.argv:
        try:
            seg_frac = float(sys.argv[sys.argv.index("-sf")+1])
            print("seg_frac = ", seg_frac)
            config.append({"string":"SF"+str(seg_frac), "pretraining": False})
        except:
            print("ERROR: unable to find segmentation fraction number USING DEFAULT VALUE", seg_frac)


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
        new = True

    nn_config = {
        "name": name,
        "config": config,
    }

    pt_test = False
    max_episodes = 25000
    if "-pt_test" in sys.argv:
        pt_test = True
        max_episodes = 600
        game_batch = 2*max_episodes

    run_agent = \
        run_agent.AgentRun(
            max_episodes = max_episodes,
            min_score = 100000,
            nn_layers = [[(20, 3)], [144]],
            lr = lr,                                #!!!
            lr_pt = lr_pt,
            gamma = 0.99,
            seg_frac = seg_frac,
            game_batch = game_batch,                #!!
            epochs_per_batch = epochs_per_batch,    #!!!
            new = new,
            init_epochs = init_epochs,              #!!!
            init_size = init_size,                  #qto mais, melhor
            init_batch = init_batch,
            depth = 3,
            use_screen = use_screen,
            sleep = sleep,
            config = nn_config,
            pt_test = pt_test
        )
    if not pretrain_only:
        run_agent.run()

