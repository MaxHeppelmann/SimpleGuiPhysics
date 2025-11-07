import numpy as np
import simpleguitk as sg

dt: float = 1 / 60
canvas_height=600
canvas_width=600

class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> "Vector":
        x=self.x*other
        y=self.y*other
        newVector=Vector(x,y)
        return newVector

    def get_magnitude(self) -> float:
        return np.sqrt(self.x**2 + self.y**2)

    def get_squared_magnitude(self) -> float:
        return self.x**2 + self.y**2

    def normalize(self) -> "Vector":
        mag: float = self.get_magnitude()
        if mag==0:
            self.x=0
            self.y=0
            return self
        self.x /= mag
        self.y /= mag
        return self

    @staticmethod
    def dotProduct(v1: "Vector", v2: "Vector") -> float:
        return v1.x * v2.x + v1.y * v2.y


class Particle:
    def __init__(self, x: float, y: float, velocity: Vector=Vector(0,0), radius: float = 100):
        self.position: Vector = Vector(x, y)
        self.velocity: Vector = velocity
        self.radius: float = radius

    def frameUpdate(self, canvas):
        self.velocity += gravity * dt
        self.updateVelocity()
        self.solveWorldCollision()
        for particle in Particles:
            if particle != self:
                if self.checkParticleCollision(particle):
                    self.solveOverlap(particle)
                    Particle.solveVelocityChange(self, particle)
        canvas.draw_circle((self.position.x, self.position.y), self.radius, 1, "White")

    def updateVelocity(self):
        self.position += self.velocity * dt

    def checkParticleCollision(self, other: "Particle"):
        distance_between_particles_sqr = (
            self.position - other.position
        ).get_squared_magnitude()
        return distance_between_particles_sqr < (self.radius + other.radius) ** 2

    def solveWorldCollision(self):
        if self.position.x<0+self.radius:
            self.position.x=0+self.radius
            self.velocity.x*=-1
        elif self.position.x>600-self.radius:
            self.position.x=600-self.radius
            self.velocity.x*=-1
        if self.position.y<0+self.radius:
            self.position.y=0+self.radius
            self.velocity.y*=-1
        elif self.position.y>600-self.radius:
            self.position.y=600-self.radius
            self.velocity.y*=-1
    def updatePosition(self, angle: float, distance: float):
        deltaX: float = np.cos(angle) * distance
        deltaY: float = np.sin(angle) * distance
        self.position += Vector(deltaX, deltaY)

    @staticmethod
    def findOverlapAngle(p1: "Particle", p2: "Particle") -> float:
        overlapComponent: Vector = p1.position - p2.position
        angle = np.arctan2(overlapComponent.y, overlapComponent.x)
        return angle

    @staticmethod
    def findOverlapLength(p1: "Particle", p2: "Particle"):
        return (p1.radius + p2.radius) - (p1.position - p2.position).get_magnitude()

    def solveOverlap(self, other: "Particle"):
        overlap = Particle.findOverlapLength(self, other)
        angle = Particle.findOverlapAngle(self, other)
        self.updatePosition(angle, overlap / 2)
        other.updatePosition(-angle, overlap / 2)

    @staticmethod
    def solveVelocityChange(p1: "Particle", p2: "Particle"):
        p1velocityTangent = p1.findVelocityTangent(p2)
        p2velocityTangent = p2.findVelocityTangent(p1)
        p1.velocity += p1velocityTangent * 2
        p2.velocity += p2velocityTangent * 2

    def findVelocityTangent(self, other: "Particle") -> Vector:
        tangent = self.findNormal(other)
        return self.velocity - tangent

    def findNormal(self, other):
        tangent = self.findCollisionTangent(self, other).normalize()
        dot = Vector.dotProduct(tangent, self.findRelativeVelocity(other))
        return tangent * dot

    @staticmethod
    def findCollisionTangent(p1: "Particle", p2: "Particle") -> Vector:
        return Vector(-(p1.position.x - p2.position.x), p1.position.y - p2.position.y)

    def findRelativeVelocity(self, other: "Particle") -> Vector:
        return self.velocity - other.velocity


frame = sg.create_frame("Collision Sim", canvas_width, canvas_height)
center_point = (300, 300)
animation_time: float = 0
Particles = [
    Particle(center_point[0] + x, center_point[1] + y, radius=7.5)
    for x in range(-100, 100, 20)
    for y in range(-100, 100, 20)
]
gravity = Vector(0, 9.8)


def drawHandler(canvas):
    global animation_time
    for i in range(len(Particles)):
        Particles[i].frameUpdate(canvas)
    animation_time += dt


frame.set_canvas_background("black")
frame.set_draw_handler(drawHandler)
frame.start()
