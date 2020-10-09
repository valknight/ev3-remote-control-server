import json
import time
from config import button_timeout, robot_timeout
from classes.button import Button
with open('commands.json', 'r') as f:
    default_commands = json.loads(f.read())

def get_robot(robots: list, robotId: int):
    for robot in robots:
        if robot.getRobotId() == robotId and robot.isAlive():
            return robot
    return None

class Robot():
    def __init__(self, robotName, robotId, commands=default_commands):
        self.robotName = robotName
        self.robotId = robotId
        self.inUse = False
        self.commands = commands
        self.heldButtons = []
        self.commandLog = []
        self.lastHeardFromTime = time.time() * 1000
    
    def markInUse(self):
        self.inUse = True

    def releaseRobot(self):
        self.inUse = False
    
    def checkValidityOfButtonCode(self, buttonCode: str):
        for button in self.commands:
            if button['code'] == buttonCode:
                return button
        return False
    
    def pushButton(self, button: dict):
        button = self.checkValidityOfButtonCode(button.get('code'))
        if not button:
            return False
        # delete the button if it is already held
        # this does scale linearly, yes
        # however, we have, what? less than a dozen? the most buttons a robot could have held won't cause issues.
        for i in range(0, len(self.heldButtons)):
            if self.heldButtons[i].buttonCode == button.get('code'):
                del self.heldButtons[i]
        coords = button.get('coord_mod', {})
        b = Button(button.get('code'), int(time.time()*1000), x=coords.get('x', 0), y=coords.get('y', 0), z=coords.get('z', 0))
        self.heldButtons.append(b)
        self.commandLog.append(b.toDict())
        self.writeLog()
        return b
    
    def clearUpButtons(self):
        while True:
            hasRemoved = False
            for i in range(0, len(self.heldButtons)):
                button = self.heldButtons[i]
                delay = time.time()*1000 - button.pushTime
                if delay >= button_timeout:
                    del self.heldButtons[i]
                    print("!!")
                    hasRemoved = True
            if not hasRemoved:
                break
    
    def writeLog(self):
        with open('logs/{}-{}.log.json'.format(self.getRobotId(), self.getRobotName()), 'w') as f:
            f.write(json.dumps(self.commandLog))
    
    def getCommands(self):
        return self.commands
    
    def getRobotName(self):
        return self.robotName
    
    def getRobotId(self):
        return self.robotId
    
    def getHeldButtons(self):
        buttonCodes = []
        self.clearUpButtons()
        for button in self.heldButtons:
            buttonCodes.append(button.toDict())
        return buttonCodes
    
    def getCoords(self):
        # This is the direction to which the robot is going to move
        # x = turning, z = forward / back, y = arm up / down
        coord = (0,0,0)
        for button in self.heldButtons:
            x = coord[0]
            y = coord[1]
            z = coord[2]
            x += button.coord[0]
            y += button.coord[1]
            z += button.coord[2]
            coord = (x,y,z)
        return coord
    
    def toDict(self):
        return {
            'name': self.getRobotName(),
            'id': self.getRobotId(),
            'commands': self.getCommands(),
            'buttons': self.getHeldButtons(),
            'timeSinceLastConnection': self.timeSinceLastConnection(),
            'coords': self.getCoords()
        }
    
    def alive(self):
        self.lastHeardFromTime = (time.time() * 1000)
    
    def timeSinceLastConnection(self):
        return (time.time() * 1000) - self.lastHeardFromTime
    def isAlive(self):
        return self.timeSinceLastConnection() < robot_timeout