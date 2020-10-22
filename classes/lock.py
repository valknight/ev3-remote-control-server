import time
from server.util.code import generate_code
# Time in we want to wait before marking a robot as inactive
maxTimeSinceLastRelock = 1000 #TODO: Make this work from the config


class Lock():
    def __init__(self):
        self.keys = []
        self.lastHeardFromClient = 0 # TODO: Change last heard from to be *per key*, so that we can invalidate singular keys

    def checkIfLockActive(self):
        if len(self.keys) == 0:
            return False
        isActive = time.time() - self.lastHeardFromClient < (maxTimeSinceLastRelock / 1000)
        if not isActive:
            self.keys = []
        return isActive

    def clientHeartbeat(self):
        self.lastHeardFromClient = time.time()

    def validateLock(self, key: str):
        if key in self.keys is False:
            print("!!! - Invalid key provided.")
            print(key)
            print(self.keys)
        return key in self.keys

    def generateLock(self, reset=True):
        if reset:
            self.keys = []
        new_key = generate_code(n=128, onlyInts=False)
        self.keys.append(new_key)
        self.clientHeartbeat()
        return new_key
