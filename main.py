

import pygame
from joint import Joint
from animal import Animal



pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Build snake (tail first, then reverse so joints[0] is head)
num_joints = 50
base_length = 40       # largest radius
min_tail_scale = 0.4   # tail radius will be 40% of base
max_angle = 0.7         # degrees per update, adjust as needed

joints = []

# Create tail first
tail_radius = base_length * (1 - (num_joints - 1) / num_joints * (1 - min_tail_scale))
tail = Joint(WIDTH // 2, HEIGHT // 2, tail_radius, None, max_angle=max_angle)
joints.append(tail)

# Build remaining joints toward head
for i in range(1, num_joints):
    # Gradually increase radius toward head
    scale = min_tail_scale + (i / num_joints) * (1 - min_tail_scale)
    radius = base_length * scale
    j = Joint(WIDTH // 2, HEIGHT // 2, radius, joints[i - 1], max_angle=max_angle)
    joints.append(j)

# Reverse so joints[0] is head
joints = joints[::-1]

# Slightly reduce head radius relative to second joint
if num_joints > 1:
    joints[0].radius = joints[1].radius * 0.9

snake = Animal(joints)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mx, my = pygame.mouse.get_pos()
    snake.update(mx, my)

    screen.fill((0, 0, 0))
    snake.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


"""
import pygame
from joint import Joint
from leg_joint import LegJoint
from animal import Animal

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- Creature parameters ---
num_joints = 12
head_radius = 50
neck_radius = 25
body_radius = 35
tail_radius = 8
max_angle = 0.6
leg_max_dist = 90

joints = []

# --- Build joints tail → head (next points backward) ---
for i in range(num_joints):
    # Determine radius
    if i == 0:
        radius = tail_radius
    elif 1 <= i <= 4:
        radius = body_radius
    elif i == 5:
        radius = neck_radius
    else:
        radius = head_radius

    if i == 0:
        joint = Joint(WIDTH // 2, HEIGHT // 2, radius, None, max_angle=max_angle)
    else:
        prev = joints[i - 1]
        joint = Joint(WIDTH // 2, HEIGHT // 2, radius, prev, max_angle=max_angle)
    joints.append(joint)

# Reverse so joints[0] is head
joints = joints[::-1]

# --- Place front legs (near head) ---
front_leg_index = 1  # neck joint
idx = front_leg_index
prev_joint = joints[idx + 1] if idx + 1 < len(joints) else None
prev_prev = joints[idx + 2] if idx + 2 < len(joints) else None
joints[idx] = LegJoint(
    joints[idx].x,
    joints[idx].y,
    joints[idx].radius,
    prev_joint,
    max_angle=max_angle,
    max_dist=leg_max_dist,
    prev_joint=prev_prev,
    leg_radius=30
)

# --- Place back legs (one more joint further from head) ---
back_leg_index = 4  # moved one joint further
idx = back_leg_index
prev_joint = joints[idx + 1] if idx + 1 < len(joints) else None
prev_prev = joints[idx + 2] if idx + 2 < len(joints) else None
joints[idx] = LegJoint(
    joints[idx].x,
    joints[idx].y,
    joints[idx].radius,
    prev_joint,
    max_angle=max_angle,
    max_dist=leg_max_dist,
    prev_joint=prev_prev,
    leg_radius=30
)

# --- Fix .next references for all joints ---
for i in range(len(joints) - 1):
    joints[i].next = joints[i + 1]
joints[-1].next = None  # tail has no next

# Slightly reduce head radius
joints[0].radius *= 0.9

lizard = Animal(joints)

# --- Game loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mx, my = pygame.mouse.get_pos()
    lizard.update(mx, my)

    screen.fill((30, 30, 30))
    lizard.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
"""