import numpy as np
from p5 import *
import argparse
from matplotlib import pyplot as plt

from creature import Creature
from food import Food
from preprocessor import Preprocessor

episode = 0

# Environment hyperparameters
env_area = 300
up = [0, -1]
right = [1, 0]
down = [0, 1]
left = [-1, 0]
possible_actions = [up, right, down, left]
action_size = len(possible_actions)

# Preprocessor hyperparameters
stack_size = 2
frame_size = 16

# Population hyperparameters
initial_population = 5
fov = 64
energy = 300
min_replay_size = 128
batch_size = 64
state_size = (frame_size, frame_size, stack_size*3)

# Resources hyperparameters
initial_food = 50

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
            energy,
            action_size,
            state_size
            ))
    
    # Setup food
    for i in range(initial_food):
        food.append(Food(
            np.random.randint(fov, width - fov),
            np.random.randint(fov, height - fov)))
    
    print('Setup finished')

def draw():
    global episode
    env = p5.renderer.fbuffer.read(mode='color', alpha=False)
    for c in population:
        raw_state = c.get_state(env)
        c.previous_state = c.current_state
        c.current_state, c.stacked_frames  = Preprocessor.stack_frames(raw_state, c.stacked_frames, frame_size, stack_size)
        if len(c.previous_state) > 0 :
            c.remember((c.previous_state, c.last_action, c.last_reward, c.current_state))
            if c.memory.get_length() >= min_replay_size and episode % 5 == 0:
                c.model.replay(batch_size)
            if episode % 100 == 0:
                c.model.update_target_model()
            if episode % 500 == 0:
                print('Ep: {:d} Id:{:d} Mem:{:d} Score:{:d}'.format(episode, c.id, c.memory.get_length(), c.score))
                c.score = 0

            
    background(0)
    # Draw boundaries
    no_fill()
    stroke(Color(1, 0, 0))
    rect((fov/2, fov/2), width - fov, height - fov)

    # Update entities
    for f in food:
        f.update()
        f.draw() 
            
    for c in population:
        action = c.model.act(c.previous_state)
        reward = c.update(possible_actions[action], food)
        c.last_action = action
        c.last_reward = reward
        # next_state = state
        # c.remember((state, action, reward, next_state))
        c.draw()
    episode += 1

if __name__ == '__main__':
    run(frame_rate=30)