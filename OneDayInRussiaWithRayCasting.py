import pygame
import math

# settings (danger zone!)
FPS = 30
P, Q = 16, 9
WIDTH, HEIGHT = 1920, 1080
FOV = 60

BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 220)
WHITE = (220, 220, 220)
STARTING_ANGLE = 3 * math.pi / 2
PLAYER_SPEED = 5
PLAYER_ROTATION = math.pi * 0.02
POV = math.pi * FOV / 180
NUM_RAYS = 120
SPEED_OF_LIGHT = 2
PERSPECTIVE = 0.12
TILE = WIDTH // P
SCALE = WIDTH // NUM_RAYS
STARTING_POS = (WIDTH // 2, HEIGHT // 2)
STEP = POV / NUM_RAYS
DIAMETER = 2 * max(WIDTH, HEIGHT)
MAX_DEPTH = DIAMETER

pygame.init()
clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIDTH, HEIGHT))


class Player:
    def __init__(self):
        self.x, self.y = STARTING_POS
        self.angle = STARTING_ANGLE

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            x_, y_ = self.x + PLAYER_SPEED * math.cos(self.angle), self.y + PLAYER_SPEED * math.sin(self.angle)
            if (int(x_) // TILE * TILE, int(y_) // TILE * TILE) not in wall_map:
                self.x = x_
                self.y = y_
        if keys[pygame.K_a]:
            self.angle += PLAYER_ROTATION
        if keys[pygame.K_s]:
            x_, y_ = self.x - PLAYER_SPEED * math.cos(self.angle), self.y - PLAYER_SPEED * math.sin(self.angle)
            if (int(x_) // TILE * TILE, int(y_) // TILE * TILE) not in wall_map:
                self.x = x_
                self.y = y_
        if keys[pygame.K_d]:
            self.angle -= PLAYER_ROTATION

    def pos(self):
        return int(self.x), int(self.y)


def color_in_perspective(color, depth):
    ret = []
    for x in color:
        ret.append(max(0, x - PERSPECTIVE * depth))
    return ret[0], ret[1], ret[2]


def ray_casting(curr_sc, curr_player):
    curr_angle = curr_player.angle + POV / 2
    x0, y0 = curr_player.pos()
    for ray in range(NUM_RAYS):
        for d in range(0, MAX_DEPTH, SPEED_OF_LIGHT):
            x = x0 + d * math.cos(curr_angle)
            y = y0 + d * math.sin(curr_angle)
            if (int(x) // TILE * TILE, int(y) // TILE * TILE) in wall_map:
                # pygame.draw.line(curr_sc, GREEN, curr_player.pos(), (x, y), 2)
                h = int(min(HEIGHT / 2, 100000 / d))
                pygame.draw.rect(curr_sc, color_in_perspective(BLUE, d), (ray * SCALE, HEIGHT // 2 - h, SCALE, h))
                pygame.draw.rect(curr_sc, color_in_perspective(BLUE, d), (ray * SCALE, HEIGHT // 2, SCALE, h))
                break
        curr_angle -= STEP


def insert_wall(curr_text_map, x, y):
    curr_text_map[x] = curr_text_map[x][:y] + 'w' + curr_text_map[x][(y + 1):]


# generating world...
player = Player()
text_map = ['w' * P] + ['w' + '.' * (P - 2) + 'w'] * (Q - 2) + ['w' * P]
insert_wall(text_map, 2, 1)
insert_wall(text_map, 4, 3)
insert_wall(text_map, 6, 5)
insert_wall(text_map, 8, 7)
insert_wall(text_map, 6, 10)
insert_wall(text_map, 4, 12)
insert_wall(text_map, 2, 14)
wall_map = set()
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char == 'w':
            wall_map.add((i * TILE, j * TILE))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.fill(RED)
    # for wall in wall_map:
    #     pygame.draw.rect(sc, GREEN, (wall[0], wall[1], TILE, TILE), 2)
    # pygame.draw.circle(sc, GREEN, player.pos(), 12)
    pygame.draw.rect(sc, WHITE, (0, 0, WIDTH, HEIGHT // 2))
    ray_casting(sc, player)
    player.movement()
    pygame.display.flip()
    clock.tick(FPS)
