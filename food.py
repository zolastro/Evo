import random
from p5 import *
class Food:
    def __init__(self, x, y):
        self.position = [x, y]
        self.size = 10
        self.max_size = 20

    def update(self):
        if (random.random() > 0.99):
            self.size += 1
            self.size = min(self.size, self.max_size)

    def draw(self):
        no_stroke()
        fill(Color(0, 255, 0))
        ellipse((self.position[0], self.position[1]), self.size/2, self.size/2)
    