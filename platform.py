from cmu_112_graphics import *

class Platform(object):
    def __init__(self, x, y):
        self.leftBound = x
        self.rightBound = self.leftBound + 180
        self.topBound = y
        self.bottomBound = self.topBound + 73
    