import time

class Timer(object):
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        if self.name:
            print('[%s]' % self.name,)
        print('Elapsed: %ss' % (time.time() - self.tstart))

class Timer2:
    def __init__(self):
        self.tstart = 0

    def enter(self):
        self.tstart = time.time()

    def exit(self):
        return round((time.time() - self.tstart)*1000000,2)