from math import atan2
from collections import deque

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

        self.energy -= 1
        reward = -1

        # Check if eating food
        for f in food:
            if (dist(self.position[0], self.position[1], f.position[0], f.position[1]) < (f.size + self.size)):
                reward += 5
                self.energy += 5
                f.size -= 1

    def remember(self, state, reward, action):
        print('#')
        #self.memory.append()


    def get_state(self):
            return get(int(self.position[0] - (self.fov / 2)), int(self.position[1] - (self.fov / 2)), self.fov, self.fov)


    def draw(self):
        # Calculate which angle the creature is heading
        theta = atan2(self.velocity[1], self.velocity[0]) - PI 
        pushMatrix()
        translate(self.position[0], self.position[1]);
        rotate(theta)

        # Draw the creature itself
        col = color(255, 102, 255)
        fill(col)
        stroke(col)
        beginShape()
        vertex(0, -self.size * 2)
        vertex(-self.size, self.size * 2)
        vertex(self.size, self.size * 2)
        endShape(CLOSE)
        popMatrix()
        noFill()
        stroke(col)
        rect(int(self.position[0] - (self.fov / 2)), int(self.position[1] - (self.fov / 2)), self.fov, self.fov)
