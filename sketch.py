import numpy as np
from p5 import *

from creature import Creature
from food import Food
population = []
food = []
# Parameters
initial_population = 1
initial_food = 20

def setup():
    size(300, 300)
    frameRate(30)
    colorMode(RGB, 255, 255, 255, 100)

    for i in range(initial_population):
        population.append(Creature(random(width) , random(height)))
    
    for i in range(initial_food):
            food.append(Food(random(width) , random(height)))



def draw():
    background(0)
    for f in food:
            if (f.size == 0):
                del f
            else:
                f.update()
                f.draw()

    for c in population:
        reward = c.update([0, 0], food)
        c.draw()
        state = c.get_state()
        state.resize(16, 16)
        state.filter(GRAY)
        state.loadPixels()
        print(len(state.pixels))
        for pixel in np.array(state.pixels, dtype=np.uint8):
            print(pixel)
        print('----------------------------------')
        image(state, 0, 0, 16, 16)

        #print(state.pixels)
        #c.remember(state, reward)

if __name__ == '__main__':
        run()
