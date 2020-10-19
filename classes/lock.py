import time
from server.util.code import generate_code
maxTimeSinceLastRelock = 500


class Lock():
    def __init__(self):
        self.key = None
        self.lastHeardFromClient = 0

    def checkIfLockActive(self):
        if self.key is None:
            return False
        isActive = self.lastHeardFromClient - time.time() < maxTimeSinceLastRelock
        if not isActive:
            self.key = None
        return isActive

    def validateLock(self, key: str):
        return key == self.key

    def generateLock(self):
        self.key = generate_code(n=128, onlyInts=False)
        return self.key
