import numpy as np
from p5 import *
import argparse

from creature import Creature
from food import Food
from skimage import transform
from matplotlib import pyplot as plt

# Environment hyperparameters
env_area = 300

# Population hyperparameters
initial_population = 10
fov = 64
energy = 300

# Resources hyperparameters
initial_food = 20

# Entities initialization
population = []
food = []


def setup():
    # Setup canvas and color settings 
    size(env_area + fov, env_area + fov)
    color_mode('RGB', 1, 1, 1, 1)

    # Setup initial population
    for i in range(initial_population):
        population.append(Creature(
            np.random.randint(fov, width - fov),
            np.random.randint(fov, height - fov),
            fov,
            energy
            ))
    
    # Setup food
    for i in range(initial_food):
        food.append(Food(
            np.random.randint(fov, width - fov),
            np.random.randint(fov, height - fov)))
    
    print('Setup finished')

def draw():
    with load_pixels():
        env = p5.renderer.fbuffer.read(mode='color', alpha=False)
        for c in population:
            state = c.get_state(env)
        
    background(0)
    # Draw boundaries
    no_fill()
    stroke(Color(1, 0, 0))
    rect((fov/2, fov/2), width - fov, height - fov)

    # Update entities
    for c in population:
        c.update([-0.01, 0.01], food)
        c.draw()

    for f in food:
        if (f.size == 0):
            del f
        else:
            f.update()
            f.draw() 
        
    



if __name__ == '__main__':
    run(frame_rate=30)