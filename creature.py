from math import atan2
from PIL import Image
from collections import deque
from p5 import *
import numpy as np
class Creature:

    def __init__(self, x, y):
        self.position = [x, y]
        self.velocity = [0.0, 0.0]
        self.max_speed = 8.0
        self.max_force = 0.2
#        self.memory = deque(100000)

        self.size = 3;
        self.energy = 300
        self.fov = 64


    def update(self, acceleration, food):
        # Limit force
        acc_magnitude = mag(acceleration[0], acceleration[1])
        if (acc_magnitude > self.max_force):
            acceleration[0] = (acceleration[0] * self.max_force) / acc_magnitude
            acceleration[1] = (acceleration[1] * self.max_force) / acc_magnitude


        # Update velocity
        self.velocity[0] += acceleration[0]
        self.velocity[1] += acceleration[1]
        vec_magnitude = mag(self.velocity[0], self.velocity[1])
        if (vec_magnitude > self.max_speed):
            self.velocity[0] = (self.velocity[0] * self.max_speed) / vec_magnitude
            self.velocity[1] = (self.velocity[1] * self.max_speed) / vec_magnitude

        # Update position
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        limits = 48

        self.position[0] = constrain(self.position[0], limits, width - limits)
        self.position[1] = constrain(self.position[1], limits, height - limits)

        self.energy -= 1
        reward = -1

        # Check if eating food
        for f in food:
            if (dist((self.position[0], self.position[1]), (f.position[0], f.position[1])) < (f.size + self.size)):
                reward += 5
                self.energy += 5
                f.size -= 1

    def remember(self, state, reward, action):
        print('#')
        #self.memory.append()


    def get_state(self, environment):
        left = int(self.position[0] - (self.fov / 2)) 
        right = int(self.position[0] + (self.fov / 2)) 
        top = int(self.position[1] - (self.fov / 2)) 
        bottom = int(self.position[1] + (self.fov / 2)) 
        return environment[left:right, top:bottom]

    def draw(self):
        col = Color(255, 102, 255)
        stroke(col)
        no_fill()
        square((self.position[0], self.position[1]), self.fov, 'CENTER')
        # Calculate which angle the creature is heading
        theta = atan2(self.velocity[1], self.velocity[0]) + PI/2
        push_matrix()
        translate(self.position[0], self.position[1]);
        rotate(theta)
        # Draw the creature itself
        fill(col)
        begin_shape()
        vertex(0, -self.size * 2)
        vertex(-self.size, self.size * 2)
        vertex(self.size, self.size * 2)
        end_shape('CLOSE')
        pop_matrix()

