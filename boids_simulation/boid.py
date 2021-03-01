import math
from typing import Generator

from pyglet.gl import (
    glPushMatrix, glPopMatrix, glTranslatef, glRotatef,
    glBegin, glEnd, glColor3f, glVertex2f, GL_TRIANGLES
)

from vector import Vector

# TODO: Update boid
# TODO: Extract constants
# TODO: Write unit tests

COLOR = [1.0, 1.0, 1.0]
SIZE = 10.0
BOID_RANGE = 250.0


class Boid:
    def __init__(self, position: Vector, diffs: Vector):
        self.position = position
        self.diffs = diffs
        self.history = []

    def find_nearby_boids(self, all_boids: list["Boid"]) -> Generator["Boid", None, None]:
        for boid in all_boids:
            if boid != self and self.position.distance(boid.position) < BOID_RANGE:
                yield boid
        return

    def fly_towards_center(self, boids: list["Boid"]) -> None:
        """ Aka cohesion """
        center = Vector()
        centering_factor = 0.005
        neighbors = 0

        for boid in self.find_nearby_boids(boids):
            center += boid.position
            neighbors += 1

        if neighbors:
            center /= neighbors
            self.diffs += (center - self.position) * centering_factor

    def avoid_collisions(self, boids: list["Boid"]) -> None:
        """ Aka separation """
        min_dist = 20
        avoid_factor = 0.05

        move_diff = Vector()

        for boid in boids:
            if self == boid:
                continue
            if self.position.distance(boid.position) < min_dist:
                move_diff[0] += self.position[0] - boid.position[0]
                move_diff[1] += self.position[1] - boid.position[1]

        move_diff *= avoid_factor
        self.diffs += move_diff

    def update(self, all_boids: list["Boid"]) -> None:
        # TODO: Implement
        self.fly_towards_center(all_boids)
        self.avoid_collisions(all_boids)

        for i in range(len(self.position)):
            self.position[i] += self.diffs[i]
            print(self.position)

    @staticmethod
    def render_boid():
        glBegin(GL_TRIANGLES)
        glColor3f(*COLOR)
        glVertex2f(-SIZE, 0.0)
        glVertex2f(SIZE, 0.0)
        glVertex2f(0.0, SIZE * 3.0)
        glEnd()

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], 0.0)

        glRotatef(math.degrees(math.atan2(0, 1)), 0.0, 0.0, -1.0)

        # render the boid itself
        self.render_boid()
        glPopMatrix()
