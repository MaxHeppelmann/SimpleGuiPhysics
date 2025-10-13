import simpleguitk as sg
import numpy as np
from typing import List

animation_time = 0
dt=1/120
frame = sg.create_frame("Collision Sim", 600, 600)
center_point = (300, 300)
class Vector(List[float]):
    def __init__(self,x:float,y:float):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    def get_magnitude(self):
        return np.sqrt(self.x**2 + self.y**2)
    def get_squared_magnitude(self):
        return self.x**2 + self.y**2
class Particle:
    def __init__(self,x:float,y:float,velocity:Vector,radius:float=100):
        self.position = Vector(x,y)
        self.velocity = velocity
        self.radius = radius
    def update(self):
        self.position += self.velocity
    def checkCollision(self,other):
        distance_between_particles_sqr = (self.position - other.position).get_squared_magnitude()
        return distance_between_particles_sqr <= (self.radius + other.radius)**2