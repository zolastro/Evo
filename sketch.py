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
    size(364, 364)
    color_mode('RGB', 255, 255, 255, 100)

    for i in range(initial_population):
        population.append(Creature(np.random.randint(64, width - 64) , np.random.randint(64, height - 64)))
    
    for i in range(initial_food):
        food.append(Food(np.random.randint(64, width - 64) , np.random.randint(64, height - 64)))

i = 0

def draw():
    state = None
    with load_pixels():
        for c in population:
            c.update([0.01, -0.01], food)
            state = c.get_state(pixels)

            #c.remember(state, reward)


    background(0)
    
    # Barrier
    no_fill()
    stroke(Color(255, 0, 0))
    rect((48, 48), width - 48*2, height - 48*2)
    

    for f in food:
            if (f.size == 0):
                print('kiillooo')
                del f
            else:
                f.update()
                f.draw()
    image(state, (0, 0))
    for c in population:
        c.draw()


if __name__ == '__main__':
    run(frame_rate=30)
