import math
from math import atan2, pi
from sympy import Circle, Point

from joint import Joint


def find_right_intersection(c1, c2, angle, leg_radius):

    # chat gpt helped in leg 2 placement (only the intersection method)


    points = c1.intersection(c2)



    average_x = (float(points[0].x) + float(points[1].x)) / 2
    average_y = (float(points[0].y) + float(points[1].y)) / 2

    first_angle = atan2(float(points[0].y) - average_y, float(points[0].x) - average_x)
    second_angle = atan2(float(points[1].y) - average_y, float(points[1].x) - average_x)

    if abs(angle - first_angle) < abs(angle - second_angle):
        p = points[0]
    else:
        p = points[1]

    return (float(p.x), float(p.y))


class LegJoint(Joint):
    def __init__(self, x, y, radius, next, max_angle, max_dist, prev_joint, leg_radius):
        super().__init__(x, y, radius, next, max_angle)

        self.left_leg_3 = ()
        self.right_leg_3 = ()
        self.left_leg_2 = ()
        self.right_leg_2 = ()
        self.left_leg_1 = ()
        self.right_leg_1 = ()

        self.left_leg_target = ()
        self.right_leg_target = ()
        self.max_dist = max_dist

        self.leg_radius = leg_radius

        angle = atan2(self.next.y - self.y, self.next.x - self.x)
        other_angle = 0
        r = self.radius
        dif = 0
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

        self.left_leg_target = (self.x + (r * 1.75) * math.cos(angle + pi / 2), self.y + (r * 1.75) * math.sin(angle + pi / 2))
        self.right_leg_target = (self.x + (r * 1.75) * math.cos(angle - pi / 2), self.y + (r * 1.75) * math.sin(angle - pi / 2))

        self.left_leg_3 = self.left_leg_target
        self.right_leg_3 = self.right_leg_target

        self.left_leg_1 = (self.x + r * math.cos(angle + pi/2), self.y + r * math.sin(angle + pi/2))
        self.right_leg_1 = (self.x + r * math.cos(angle - pi / 2), self.y + r * math.sin(angle - pi / 2))

        c1 = Circle(Point(self.left_leg_1[0], self.left_leg_1[1]), leg_radius + 3)
        c2 = Circle(Point(self.left_leg_3[0], self.left_leg_3[1]), leg_radius + 3)
        self.left_leg_2 = find_right_intersection(c1, c2, other_angle, leg_radius)

        c1 = Circle(Point(self.right_leg_1[0], self.right_leg_1[1]), leg_radius + 3)
        c2 = Circle(Point(self.right_leg_3[0], self.right_leg_3[1]), leg_radius + 3)
        self.right_leg_2 = find_right_intersection(c1, c2, other_angle, leg_radius)





        self.next.x = new_x
        self.next.y = new_y



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

        self.left_leg_target = (self.x + (r * 1.75) * math.cos(angle + pi/2), self.y + (r * 1.75) * math.sin(angle + pi/2))
        self.right_leg_target = (self.x + (r * 1.75) * math.cos(angle - pi/2), self.y + (r * 1.75) * math.sin(angle - pi/2))

        if math.dist(self.left_leg_target, self.left_leg_3) > self.max_dist:
            self.left_leg_3 = self.left_leg_target

        if math.dist(self.right_leg_target, self.right_leg_3) > self.max_dist:
            self.right_leg_3 = self.right_leg_target

        self.next.x = new_x
        self.next.y = new_y

        self.fabrik(15)

    def set_next(self, next):
        self.next = next

    def fabrik(self, times):

        for i in range(times):

            if i%2 == 0:

                self.left_leg_3 = self.left_leg_target

                angle = atan2(self.left_leg_3[1] - self.left_leg_2[1], self.left_leg_3[0] - self.left_leg_2[0])
                r = self.leg_radius

                new_x = self.left_leg_2[0] + r * math.cos(angle)
                new_y = self.left_leg_2[1] + r * math.sin(angle)

                self.left_leg_2 = (new_x, new_y)


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

                self.right_leg_3 = self.right_leg_target


                angle = atan2(self.right_leg_3[1] - self.right_leg_2[1], self.right_leg_3[0] - self.right_leg_2[0])
                r = self.leg_radius

                new_x = self.right_leg_2[0] + r * math.cos(angle)
                new_y = self.right_leg_2[1] + r * math.sin(angle)

                self.right_leg_2 = (new_x, new_y)
            else:
                self.left_leg_2 = self.left_leg_target


                angle = atan2(self.left_leg_3[1] - self.left_leg_2[1], self.left_leg_3[0] - self.left_leg_2[0])
                r = self.leg_radius

                new_x = self.left_leg_2[0] + r * math.cos(angle)
                new_y = self.left_leg_2[1] + r * math.sin(angle)

                self.left_leg_2 = (new_x, new_y)

                # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

                angle = atan2(self.right_leg_3[1] - self.right_leg_2[1], self.right_leg_3[0] - self.right_leg_2[0])
                r = self.leg_radius

                new_x = self.right_leg_2[0] + r * math.cos(angle)
                new_y = self.right_leg_2[1] + r * math.sin(angle)

                self.right_leg_2 = (new_x, new_y)

