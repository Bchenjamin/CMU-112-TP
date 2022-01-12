from cmu_112_graphics import *

class Character(object):
    def __init__(self, x, y, velocityX, velocityY):
        self.x = x
        self.y = y
        self.xv = velocityX
        self.yv = velocityY
        self.powerUps = []
    
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def move(self, x, y): 
        self.x += x
        self.y += y
        self.xv = x


    
