import numpy as np
from p5 import *
import argparse
from matplotlib import pyplot as plt

from creature import Creature
from food import Food
from preprocessor import Preprocessor

# Environment hyperparameters
env_area = 300
stacked_state = []
stacked_frames = []
# Preprocessor hyperparameters
stack_size = 2
frame_size = 16

# Population hyperparameters
initial_population = 1
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
    global stacked_state
    global stacked_frames
    env = p5.renderer.fbuffer.read(mode='color', alpha=False)
    for c in population:
        state = c.get_state(env)
        stacked_state, stacked_frames  = Preprocessor.stack_frames(state, stacked_frames, 16, 2)
    background(0)
    # Draw boundaries
    no_fill()
    stroke(Color(1, 0, 0))
    rect((fov/2, fov/2), width - fov, height - fov)

    # Update entities
    for f in food:
        if (f.size == 0):
            del f
        else:
            f.update()
            f.draw() 
            
    for c in population:
        c.update([-0.01, 0.01], food)
        c.draw()


if __name__ == '__main__':
    run(frame_rate=30)