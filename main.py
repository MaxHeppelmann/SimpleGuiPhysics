import simpleguitk as simplegui
import math

animation_time = 0
frame = simplegui.create_frame("Optical Illusion", 600, 600)
center_point = (300, 300)
R: int = 300  # Radius of the larger circle
r: float = R / 2  # Radius of the smaller circle, remains half in order to demonstrate optical illusion


class Point:
    def __init__(self, angle, t):
        self.x = center_point[0]
        self.y = center_point[1]
        self.offset = angle  # Offset angle for each point
        self.update(t)

    def update(self, t):
        # Update point coordinates based on parametric equations
        self.x = center_point[0] + (R - r) * math.cos(t) + r * math.cos(-t + self.offset)
        self.y = center_point[1] + (R - r) * math.sin(t) + r * math.sin(-t + self.offset)


# Animation handler function
def draw_handler(canvas):
    global animation_time
    animation_time += 0.02  # Increment time to animate the motion
    if animation_time < 10:
        # Draw the larger circle
        canvas.draw_circle(center_point, R, 5, "white")

        # Generate points
        num_of_points: int = 16
        points = [Point(i * 2 * math.pi / num_of_points, animation_time) for i in range(num_of_points)]  # num_of_points evenly spaced points

        # Draw all points
        for point in points:
            canvas.draw_circle((point.x, point.y), 10, 5, "white")  # Draw each point
    else:
        canvas.draw_circle(center_point, R, 5, "white")
        one_point = Point(0, animation_time)
        canvas.draw_line((0, 300), (600, 300), 5, "red")
        canvas.draw_circle((one_point.x, one_point.y), 10, 5, "white")


frame.set_canvas_background("black")
frame.set_draw_handler(draw_handler)
frame.start()
