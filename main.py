from collections import deque
import sys
import pygame
from time import sleep
pygame.init()

SCALE = 2 # 1 for 1080p 2 for 2160p
SIZE = WIDTH, HEIGHT = (800*SCALE, 800*SCALE)

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SQUARE_SCALE = 8*SCALE # size of squares

def gen_walls():
    outer_walls = [(i, 0) for i in range(1, 99)] + [(i, 99) for i in range(1, 99)] + \
        [(0, i) for i in range(1, 99)] + [(99, i) for i in range(1, 99)]
    inner_walls = [(i, 48) for i in range(48, 52)] + [(i, 51) for i in range(48, 52)] + \
        [(48, i) for i in range(49, 51)] + [(51, i) for i in range(49, 51)]
    return tuple(outer_walls + inner_walls)

WALLS = gen_walls()

screen = pygame.display.set_mode(SIZE)
dir_buffer = deque(['r'])
snake_segs = [(10, 10)]
snake_length = 1

game_over = False

DIR_MAP = {
    pygame.K_LEFT: 'l',
    pygame.K_RIGHT: 'r',
    pygame.K_UP: 'u',
    pygame.K_DOWN: 'd',
}

OPPOSITE_MAP = {
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

    if key in DIR_MAP:
        if dir_buffer[-1] != DIR_MAP[key] and OPPOSITE_MAP[dir_buffer[-1]] != DIR_MAP[key]:
            dir_buffer.append(DIR_MAP[key])

    # DEBUG
    if key == pygame.K_SPACE:
        increase_snake_length()


def check_collision():
    global game_over

    collision = False
    if snake_segs[0] in snake_segs[1:] or snake_segs[0] in WALLS:
        collision = True

    if collision:
        game_over = True


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
        pygame.draw.rect(screen, GREEN, [seg_x*SQUARE_SCALE, seg_y*SQUARE_SCALE, SQUARE_SCALE, SQUARE_SCALE])


def render_walls():
    for i in range(0, len(WALLS)):
        wall_x, wall_y = WALLS[i]
        pygame.draw.rect(screen, BLUE, [wall_x*SQUARE_SCALE, wall_y*SQUARE_SCALE, SQUARE_SCALE, SQUARE_SCALE])


def render_game_area():
    render_walls()
    render_snake()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            keyboard_event(event.key)

    move_snake()
    check_collision()

    # Handle rendering bits
    screen.fill(BLACK)
    render_game_area()

    if game_over:
        font = pygame.font.Font(None, 36*SCALE)
        text = font.render("Game Over - Press ESC for new game", 1, RED)
        textpos = text.get_rect(centerx=WIDTH/2, centery=HEIGHT/4)
        screen.blit(text, textpos)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    dir_buffer = deque(['r'])
                    snake_segs = [(10, 10)]
                    snake_length = 1
                    game_over = False

            if not game_over:
                break
            sleep(0.5)

    else:
        pygame.display.flip()
        sleep(0.1)