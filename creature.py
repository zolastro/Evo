from p5 import *
from math import atan2

from DDQN import DDQN
from replay_buffer import ReplayBuffer

class Creature:
    id = 0

    def __init__(self, x, y, fov, energy, action_size, state_size):
        self.id = Creature.id
        Creature.id += 1
        # Memories
        self.stacked_frames = []
        self.current_state = []
        self.last_action = []
        self.last_reward = 0
        self.previous_state = []
        self.memory = ReplayBuffer(50000)
        self.score = 0
    
        # Model
        self.model = DDQN(state_size, action_size, self.memory)

        # Attributes
        self.position = [x, y]
        self.energy = 300
        self.fov = fov
        self.velocity = [0.0, 0.0]
        self.max_speed = 2.0
        self.max_force = 0.2
        self.size = 3

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

        # Add boundaries of the size of fov
        self.position[0] = constrain(self.position[0], self.fov/2, width - self.fov/2)
        self.position[1] = constrain(self.position[1], self.fov/2, height - self.fov/2)

        # Decrease energy every step

        reward = -1

        # Check if it is eating food
        for f in food:
            if ((f.size > 0) and dist((self.position[0], self.position[1]), (f.position[0], f.position[1])) < (f.size + self.size)):
                reward += 5
                self.score += 5
                f.size -= 1
        return reward

    def get_state(self, environment):
        left = int(self.position[0] - (self.fov / 2)) 
        right = int(self.position[0] + (self.fov / 2)) 
        top = int(self.position[1] - (self.fov / 2)) 
        bottom = int(self.position[1] + (self.fov / 2)) 
        return environment[top:bottom, left:right, :]

    def draw(self):
        col = Color(1, 0.4, 1)
        stroke(col)
        
        # Draw fov for debugging
        # no_fill()
        # square((self.position[0], self.position[1]), self.fov, 'CENTER')
        
        # Calculate which angle the creature is heading
        theta = atan2(self.velocity[1], self.velocity[0]) + PI/2
        
        # Draw the creature itself
        translate(self.position[0], self.position[1]);
        rotate(theta)
        fill(col)
        begin_shape()
        vertex(0, -self.size * 2)
        vertex(-self.size, self.size * 2)
        vertex(self.size, self.size * 2)
        end_shape('CLOSE')
        reset_matrix()

    def remember(self, experience):
        self.memory.store_experience(experience)

