"""
Program common module.

This module can be imported to all modules to provide common
access to container / object definitions for modules.
"""

class vecXY:
    """A simple two dimensional vector container"""
    __vecX = 0.00
    __vecY = 0.00

    def set(self, nXY=[0.0, 0.0]):
        """Set the velocity values"""
        self.__vecX = nXY[0]
        self.__vecY = nXY[1]

    def sum(self, sXY=[0.0,0.0]):
        """Sum onto the current velocity values, pass as set"""
        self.__vecX += sXY[0]
        self.__vecY += sXY[1]

    def get(self, sel=None):
        """Returns the current velocity, either in a set or individually [None, 0, 1]"""
        if (sel == None):
          return [self.__vecX, self.__vecY]
        elif sel == 0:
          return self.__vecX
        else:
          return self.__vecY

class PointCharge:
    """Point charge class definition, used in calculation/simulation/rendering"""
    # Attributes
    pMass = 0.00  # Point Mass
    pCharge = 0.00  # Point Charge
    pRadius = 5.00  # Point Radius, should remain constant
    pPos = vecXY()  # Position vector
    pVel = vecXY()  # Velocity vector
    pAcc = vecXY()  # Acceleration vector

    pNetF = vecXY()  # Net force vector
    pIdvF = []  # Individual force vectors

    # Methods
    def __init__(self, jsonData=None):
        """Point object init, if JSON data is provided, populate, else use defaults"""
        if jsonData != None:
            # Populate object with data from JSON DOM.
            self.pMass = jsonData["mass"]
            self.pCharge = jsonData["charge"]
            self.pPos.set(jsonData["pos"])
            self.pVel.set(jsonData["vel"])


    def updateVel(self, deltaTime):
        """Update velocity based on current instantaneous acceleration and provided sim delta time"""
        addX = self.pAcc.get(0) * deltaTime
        addY = self.pAcc.get(1) * deltaTime
        self.pPos.sum([addX, addY])

    def updatePos(self, deltaTime):
        """Update velocity based on current instantaneous acceleration and provided sim delta time"""
        addX = self.pVel.get(0) * deltaTime
        addY = self.pVel.get(1) * deltaTime
        self.pPos.sum([addX, addY])

    def updateNetF(self, deltaTime):
        """Sum the current net force based on individual forces"""
        for i in range(len(self.pIdvF)):
            self.pNetF.sum(self.pIdvF[0].get())

    def getJSON(self):
        """Returns the JSON dictionary for save functionality"""
        #TODO: Expand stub
        #TODO: Write cyclic test to check result is same as input.

