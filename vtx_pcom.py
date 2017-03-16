"""
Program common module.

This module can be imported to all modules to provide common
access to container / object definitions for modules.
"""

class vecXY:
    """A simple two dimensional vector container"""
    __vecX = 0.00
    __vecY = 0.00

    def set(self, nX, nY):
        """Set the velocity values"""
        self.__vecX = nX
        self.__vecY = nY

    def sum(self, sX, sY):
        """Sum onto the current velocity values"""
        self.__vecX += sX
        self.__vecY += sY

    def get(self, xy = None):
        """Returns the current velocity, either in a set or individually"""
        if (xy == None):
          return [self.__vecX, self.__vecY]
        elif xy == 0:
          return self.__vecX
        else:
          return self.__vecY