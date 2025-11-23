import math

import pygame

from leg_joint import LegJoint


class Animal:
    def __init__(self, joints):

        self.joints = joints

    def update(self, x, y):
        self.joints[0].x = x
        self.joints[0].y = y

        self.joints[0].update()

        for i in range(len(self.joints) - 2):
            self.joints[i + 1].update(self.joints[i])

    def draw(self, screen):
        left_body = []
        right_body = []

        num_joints = len(self.joints)

        # Build left/right points for body edge
        for i, joint in enumerate(self.joints):
            if joint.next is not None:
                dx = joint.next.x - joint.x
                dy = joint.next.y - joint.y
                length = (dx ** 2 + dy ** 2) ** 0.5
                if length != 0:
                    perp_x = -dy / length
                    perp_y = dx / length
                else:
                    perp_x = perp_y = 0

                left_body.append((joint.x + perp_x * joint.radius,
                                  joint.y + perp_y * joint.radius))
                right_body.append((joint.x - perp_x * joint.radius,
                                   joint.y - perp_y * joint.radius))
            else:
                prev = self.joints[i - 1]
                dx = joint.x - prev.x
                dy = joint.y - prev.y
                length = (dx ** 2 + dy ** 2) ** 0.5
                if length != 0:
                    perp_x = -dy / length
                    perp_y = dx / length
                else:
                    perp_x = perp_y = 0

                left_body.append((joint.x + perp_x * joint.radius,
                                  joint.y + perp_y * joint.radius))
                right_body.append((joint.x - perp_x * joint.radius,
                                   joint.y - perp_y * joint.radius))

        # Draw body polygon
        polygon_points = left_body + right_body[::-1]
        body_color = (150, 255, 150)
        pygame.draw.polygon(screen, body_color, polygon_points)
        pygame.draw.lines(screen, (50, 50, 50), True, polygon_points, 2)

        # Draw snake head (blunt)
        head = self.joints[0]
        if num_joints > 1:
            second = self.joints[1]
            dx = head.x - second.x
            dy = head.y - second.y
            length = (dx ** 2 + dy ** 2) ** 0.5
            if length != 0:
                perp_dx = -dy / length
                perp_dy = dx / length
            else:
                perp_dx = perp_dy = 0

            # Front blunt points
            front_left = (head.x + dx / length * head.radius * 1.5 + perp_dx * head.radius * 0.5,
                          head.y + dy / length * head.radius * 1.5 + perp_dy * head.radius * 0.5)
            front_right = (head.x + dx / length * head.radius * 1.5 - perp_dx * head.radius * 0.5,
                           head.y + dy / length * head.radius * 1.5 - perp_dy * head.radius * 0.5)
            # Middle head side points
            left_mid = (head.x + perp_dx * head.radius * 0.7,
                        head.y + perp_dy * head.radius * 0.7)
            right_mid = (head.x - perp_dx * head.radius * 0.7,
                         head.y - perp_dy * head.radius * 0.7)
            # Back points (blend into body)
            left_back = (head.x + perp_dx * head.radius * 0.4 - dx / length * head.radius * 0.2,
                         head.y + perp_dy * head.radius * 0.4 - dy / length * head.radius * 0.2)
            right_back = (head.x - perp_dx * head.radius * 0.4 - dx / length * head.radius * 0.2,
                          head.y - perp_dy * head.radius * 0.4 - dy / length * head.radius * 0.2)

            head_points = [front_left, front_right, right_mid, right_back, left_back, left_mid]
            pygame.draw.polygon(screen, body_color, head_points)
            pygame.draw.polygon(screen, (50, 50, 50), head_points, 2)

            # Draw eyes
            eye_offset_forward = 0.7 * head.radius
            eye_offset_side = 0.3 * head.radius

            eye1_x = head.x + dx / length * eye_offset_forward + perp_dx * eye_offset_side
            eye1_y = head.y + dy / length * eye_offset_forward + perp_dy * eye_offset_side
            eye2_x = head.x + dx / length * eye_offset_forward - perp_dx * eye_offset_side
            eye2_y = head.y + dy / length * eye_offset_forward - perp_dy * eye_offset_side

            eye_radius = int(head.radius * 0.2)
            pygame.draw.circle(screen, (255, 255, 255), (int(eye1_x), int(eye1_y)), eye_radius)
            pygame.draw.circle(screen, (255, 255, 255), (int(eye2_x), int(eye2_y)), eye_radius)
            pygame.draw.circle(screen, (0, 0, 0), (int(eye1_x), int(eye1_y)), eye_radius // 2)
            pygame.draw.circle(screen, (0, 0, 0), (int(eye2_x), int(eye2_y)), eye_radius // 2)

        # Draw legs if any
        leg_color = (150, 255, 150)
        leg_width = 6
        for i, joint in enumerate(self.joints):
            if isinstance(joint, LegJoint):
                pygame.draw.line(screen, leg_color, joint.left_leg_1, joint.left_leg_2, leg_width)
                pygame.draw.line(screen, leg_color, joint.left_leg_2, joint.left_leg_3, leg_width)
                pygame.draw.line(screen, leg_color, joint.right_leg_1, joint.right_leg_2, leg_width)
                pygame.draw.line(screen, leg_color, joint.right_leg_2, joint.right_leg_3, leg_width)
