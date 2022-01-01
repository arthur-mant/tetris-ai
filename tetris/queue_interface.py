import queue

class interface_queue:
    q = None

    def __init__(self):
        self.q = queue.SimpleQueue()

    def rotate(self, num):
        for i in range(num % 4):
            self.q.put('R')

    def move(self, num):
        for i in range(-num):
            self.q.put('E')
        for i in range(num):
            self.q.put('D')


    def go_down(self, num):
        for i in range(num):
            self.q.put('B')

    def hard_drop(self):
        self.q.put('Q')

    def exec_command(self, game):
        aux = None
        try:
            aux = self.q.get(block=False)
        except queue.Empty:
            return None
        except Exception as e:
            print("Unexpected exception in interface queue: ", e)

        if aux == 'R':
            game.rotate()
        elif aux == 'E':
            game.go_side(-1)
        elif aux == 'D':
            game.go_side(1)
        elif aux == 'B':
            game.go_down()
        elif aux == 'Q':
            game.hard_drop()
        elif aux == None:
            pass
        else:
            print("Unexpected entry in interface_queue: ",  aux)
