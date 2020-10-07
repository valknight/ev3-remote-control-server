class Button():
    def __init__(self, buttonCode: str, pushTime: int, x : int = 0, y: int = 0, z : int = 0):
        self.buttonCode = buttonCode
        self.pushTime = pushTime
        self.coord = (x,y,z)
    
    def toDict(self):
        return {
            'time': self.pushTime,
            'code': self.buttonCode,
            'coord': self.coord
        }