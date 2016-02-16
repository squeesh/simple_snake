from collections import deque
import sys
import pygame
from time import sleep
pygame.init()

scale = 2 # 1 for 1080p 2 for 2160p
size = width, height = (800*scale, 800*scale)
x_pos = 1
y_pos = 1
speed = 10

black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

screen = pygame.display.set_mode(size)

dir_buffer = deque(['r'])
seg_offset = 8*scale # size of snake segments
snake_segs = [(10, 10)]
snake_length = 1

dir_map = {
    pygame.K_LEFT: 'l',
    pygame.K_RIGHT: 'r',
    pygame.K_UP: 'u',
    pygame.K_DOWN: 'd',
}

opposite_map = {
    'l': 'r',
    'r': 'l',
    'u': 'd',
    'd': 'u',
}


def increase_snake_length():
    global snake_length
    snake_length += 1
    snake_segs.append((-1, -1)) # add just off screen ... this is a hack :(


def keyboard_event(key):
    global snake_length

    if key in dir_map:
        if dir_buffer[-1] != dir_map[key] and opposite_map[dir_buffer[-1]] != dir_map[key]:
            dir_buffer.append(dir_map[key])

    # DEBUG
    if key == pygame.K_SPACE:
        increase_snake_length()


def move_snake():
    if len(dir_buffer) > 1:
        dir_buffer.popleft()

    direction = dir_buffer[0]

    snake_x, snake_y = snake_segs[0]
    if direction == 'r':
        snake_x += 1
    elif direction == 'l':
        snake_x -= 1
    elif direction == 'd':
        snake_y += 1
    elif direction == 'u':
        snake_y -= 1

    for i in range(snake_length-2, -1, -1):
        snake_segs[i+1] = snake_segs[i]

    snake_segs[0] = (snake_x, snake_y)


def render_snake():
    for i in range(0, snake_length):
        seg_x, seg_y = snake_segs[i]
        pygame.draw.rect(screen, green, [seg_x*seg_offset, seg_y*seg_offset, seg_offset, seg_offset])


def render_game_area():
    render_snake()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            keyboard_event(event.key)

    move_snake()

    # Handle rendering bits
    screen.fill(black)
    render_game_area()
    pygame.display.flip()
    sleep(0.1)