import heapq
import random

import pygame
import numpy as np

pygame.init()

WALLS = []
WIDTH = 800
HEIGHT = 600
SIZE = 10
LINEAR_COST = 1
DIAGONAL_COST = 2
RANDOM_WALLS_RATE = 0.2

wallsColor = (255, 255, 255)
pathColor = (0, 0, 255)
route = []


class Grid:
    dimension = (160, 120)

    def __init__(self):
        self.vertical_line = pygame.Surface((1, HEIGHT))
        self.vertical_line.fill((255, 255, 255))
        self.horizontal_line = pygame.Surface((WIDTH, 1))
        self.horizontal_line.fill((255, 255, 255))

    def blit(self, screen):
        for i in range(0, WIDTH, SIZE):
            screen.blit(self.vertical_line, (i, 0))
        for i in range(0, HEIGHT, SIZE):
            screen.blit(self.horizontal_line, (0, i))


class Start:

    def __init__(self, position=(0,0)):
        self.position = (int(position[0]/SIZE)*SIZE, int(position[1]/SIZE)*SIZE)
        self.texture = pygame.Surface((SIZE, SIZE))
        self.texture.fill((0, 255, 0))

    def blit(self, screen):
        screen.blit(self.texture, self.position)


class End():

    def __init__(self, position=(WIDTH-SIZE, HEIGHT-SIZE)):
        self.position = (int(position[0]/SIZE)*SIZE, int(position[1]/SIZE)*SIZE)
        self.texture = pygame.Surface((SIZE, SIZE))
        self.texture.fill((255, 0, 0))

    def blit(self, screen):
        screen.blit(self.texture, self.position)


def blit_walls(screen):
    texture = pygame.Surface((SIZE, SIZE))
    texture.fill(wallsColor)
    for position in WALLS:
        screen.blit(texture, position)


def heuristic(current, destination):
    dx = abs(current[0] - destination[0])
    dy = abs(current[1] - destination[1])
    return LINEAR_COST * (dx + dy) + (DIAGONAL_COST - 2 * LINEAR_COST) * min(dx, dy)
    #return ((current[0] - destination[0]) ** 2) + ((current[1] - destination[1]) ** 2) No move cost difference


def find_optimal_path(array, start, goal):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []

            while current in came_from:
                data.append((current[0] * SIZE, current[1] * SIZE))
                current = came_from[current]
            return data
        close_set.add(current)

        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j

            tentative_g_score = gscore[current] + heuristic(current, neighbor)

            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return []


def generate_maze():
    maze = []
    for i in range(0, WIDTH, SIZE):
        list = []
        for j in range(0, HEIGHT, SIZE):
            if (i, j) in WALLS:
                value = 1;
            else:
                value = 0;
            list.append(value)
        maze.append(list)
    return np.array(maze)


def print_path(screen, path):
    texture = pygame.Surface((SIZE, SIZE))
    texture.fill(pathColor)
    if path:
        for node in path:
            screen.blit(texture, node)


def generate_ramdom_obstacles():
    WALLS.clear()
    route.clear()
    w = int(WIDTH / SIZE)
    h = int(HEIGHT / SIZE)
    count = 0

    while count < int(w * h * RANDOM_WALLS_RATE):
        r = (random.randint(0, w-1) * SIZE, random.randint(0, h-1) * SIZE)
        if r not in WALLS and r != s.position and r != e.position:
            WALLS.append(r)
            count += 1


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* path finder | Press 'Space' to start")
clock = pygame.time.Clock()

grid = Grid()
s = Start()
e = End()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            pos = (int(pos[0]/SIZE)*SIZE, int(pos[1]/SIZE)*SIZE)
            if pos not in WALLS and pos != s.position and pos != e.position:
                WALLS.append(pos)
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            pos = (int(pos[0] / SIZE) * SIZE, int(pos[1] / SIZE) * SIZE)
            if pos not in WALLS and pos != s.position and pos != e.position:
                WALLS.append(pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                route.clear()
                start_coordinates = (int(s.position[0] / SIZE), int(s.position[1] / SIZE))
                end_coordinates = (int(e.position[0] / SIZE), int(e.position[1] / SIZE))
                route = find_optimal_path(generate_maze(), start_coordinates, end_coordinates)
            elif event.key == pygame.K_c:
                pos = pygame.mouse.get_pos()
                pos = (int(pos[0] / SIZE) * SIZE, int(pos[1] / SIZE) * SIZE)
                if pos in WALLS:
                    WALLS.remove(pos)
            elif event.key == pygame.K_r:
                generate_ramdom_obstacles()
            elif event.key == pygame.K_s:
                show_exploration = not show_exploration
                if show_exploration:
                    pygame.display.set_caption("A* path finder | Show exploration: ON")
                else:
                    pygame.display.set_caption("A* path finder | Show exploration: OFF")
        if event.type == pygame.QUIT:
            exit()
    screen.fill((25, 25, 25))
    print_path(screen, route)
    s.blit(screen)
    e.blit(screen)
    grid.blit(screen)
    blit_walls(screen)
    pygame.display.update()