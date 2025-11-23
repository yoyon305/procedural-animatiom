import math
from math import atan2, pi


class Joint:
    def __init__(self, x, y, radius, next, max_angle):
        self.x = x
        self.y = y
        self.radius = radius
        self.next = next
        self.max_angle = max_angle


    def update(self, prev_joint=None):

        angle = atan2(self.next.y - self.y, self.next.x - self.x)
        r = self.radius

        if prev_joint:
            # Angle from prev_joint to this joint
            other_angle = atan2(self.y - prev_joint.y, self.x - prev_joint.x)

            # Compute difference
            diff = angle - other_angle

            # Normalize difference to [-pi, pi]
            while diff > pi:
                diff -= 2 * pi
            while diff < -pi:
                diff += 2 * pi

            # Clamp by max_angle
            if diff > self.max_angle:
                angle = other_angle + self.max_angle
            elif diff < -self.max_angle:
                angle = other_angle - self.max_angle

        new_x = self.x + r * math.cos(angle)
        new_y = self.y + r * math.sin(angle)


        self.next.x = new_x
        self.next.y = new_y

    def set_next(self, next):
        self.next = next
