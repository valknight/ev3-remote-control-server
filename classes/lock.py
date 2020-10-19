import time
from server.util.code import generate_code
maxTimeSinceLastRelock = 500

class Lock():
    def __init__():
        self.key = None
        self.lastHeardFromClient = 0
    
    def checkIfLockActive():
        if self.key is None:
            return False
        isActive = self.lastHeardFromClient - time.time() < maxTimeSinceLastRelock
        if not isActive:
            self.key = None
        return isInactive
    
    
    def validateLock(key: str):
        return key == self.key
    
    def generateLock():
        self.key = generate_code(n=128, onlyInts=False)
        return "a" //TODO: Make me randomly generated!