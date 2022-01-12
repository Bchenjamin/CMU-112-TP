from cmu_112_graphics import *
from powerup import *

class TimeSlow(PowerUp):
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.timeLeft = time