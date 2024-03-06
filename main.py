"""
This file contains the code for the simulation part of the project

The project used pygame for graphics
install using: pip install pygame

Features of the simulation:
1. Map the best fishing path for each day
2. Show the graph of reward vs path per iteration
"""

import pygame as pg
import sys
import random
import q_learning
import threading


# Variables for the width and height of the simulation window
WIDTH = 800
HEIGHT = 800

# Variable for the width and the height of the simulation inside the main window
# Must be <= HEIGHT and WIDTH
GRID_WIDTH = WIDTH
GRID_HEIGHT = HEIGHT-100
FPS = 100

# RGB values of colours
white = (255,255,255)
sea_blue = (50, 152, 168)
darker_blue = (50, 76, 168)

# Initialising pygame window
pg.init()
pg.display.init()
pg.display.set_caption("DeepLearningWeek")
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()


# Each cell in a grid will have these attributes
class GridCell:
    def __init__(self):
        self.qvals = [0, 0, 0, 0, 0, 0]


class OceanEnvironment:
    def __init__(self, row, col, no_row, no_col, mode):
        self.current_row = row
        self.current_col = col

        self.max_rows = no_row-1
        self.max_cols = no_col-1

        if mode == 0:
            self.fish_population = self.fish_pop_generator()
        else:
            self.fish_population = self.random_pop_generator()
        self.environment_val = 0

        self.population_history = []

    def fish_pop_generator(self):
        dist_from_shore_y = abs(self.max_rows-self.current_row)
        dist_from_shore_x = abs(self.max_cols-self.current_col)

        diag_dist = pow(pow(dist_from_shore_x,2)+pow(dist_from_shore_y,2), 0.5)
        max_dist = pow(pow(self.max_rows,2)+pow(self.max_cols,2), 0.5)
        fish_pop = int((255/max_dist)*diag_dist)
        return fish_pop

    def random_pop_generator(self):
        return random.randint(0,255)


# All the properties of the boat
class Boat:
    def __init__(self, grid):
        # position is the grid coordinates of the boat
        self.reset_pos = (len(grid)//2, len(grid)-1)

        self.pos = list(self.reset_pos)

        self.fuel_used = 0
        self.grid = grid

    def move_up(self):
        if self.pos[1] > 0:
            self.pos[1] -= 1
            self.render()
            return True
        return False

    def move_down(self):
        if self.pos[1] < len(self.grid)-1:
            self.pos[1] += 1
            self.render()
            return True
        return False

    def move_left(self):
        if self.pos[0] > 0:
            self.pos[0] -= 1
            self.render()
            return True
        return False

    def move_right(self):
        if self.pos[0] < len(self.grid)-1:
            self.pos[0] += 1
            self.render()
            return True
        return False

    def fish(self):
        decline = 10
        self.grid[self.pos[0]][self.pos[1]].fish_population -= decline

    def dock(self):
        if self.pos == list(self.reset_pos):
            return False
        if self.pos[1] == len(self.grid[0])-1:
            return True
        return False

    def render(self):
        cell_width = GRID_WIDTH / len(self.grid[0])
        cell_height = GRID_HEIGHT / len(self.grid)
        rect = (cell_width*self.pos[0], cell_height*self.pos[1], cell_width, cell_height)
        pg.draw.rect(screen, white, rect)
        pg.display.update(pg.Rect(rect))


# Creating 2-D array
def create_grid(rows, columns, mode):
    qval_grid = [[GridCell() for j in range(columns)] for i in range(rows)]
    environment_grid = [[OceanEnvironment(i, j, rows, columns, mode) for j in range(columns)] for i in range(rows)]
    return qval_grid, environment_grid


def avg_fish_population(envGrid):
    n = len(envGrid)*len(envGrid[0])
    pop = 0
    for row in envGrid:
        for cell in row:
            pop += cell.fish_population

    return int(pop/n)


pg.font.init()
my_font = pg.font.SysFont('Comic Sans MS', 9)

# Rendering the grid on screen
def render_grid(grid, Qtable):
    x_pos = 0
    y_pos = 0

    no_rows = len(grid)
    no_cols = len(grid[0])
    cell_width = GRID_WIDTH/no_cols
    cell_height = GRID_HEIGHT/no_rows

    for i in range(no_rows):
        for j in range(no_cols):
            rect = cell_width*j, cell_height*i, cell_width, cell_height
            pg.draw.rect(screen, (0, 0, abs(grid[i][j].fish_population-255)), rect)

            qv = Qtable[i][j].qvals
            mx = max(qv)
            ind = qv.index(mx)
            text_surface = my_font.render(f"{round(mx, 2)}, {ind}", True, (255, 255, 255))

            screen.blit(text_surface, (cell_width*j,cell_height*i))

    for row in grid:
        pg.draw.rect(screen, darker_blue, rect=(0, y_pos, GRID_WIDTH, 1))
        y_pos += cell_height

    for column in grid[0]:
        pg.draw.rect(screen, darker_blue, (x_pos, 0, 1, GRID_HEIGHT))
        x_pos += cell_width

    pg.draw.rect(screen, darker_blue, rect=(0, y_pos, GRID_WIDTH, 1))
    pg.draw.rect(screen, darker_blue, (x_pos, 0, 1, GRID_HEIGHT))

    pg.display.update(pg.Rect(0, 0, GRID_WIDTH+1, GRID_HEIGHT+1))


no_rows = 25
no_cols = 25

mode = 0

Qtable, environment_grid = create_grid(no_rows, no_cols, mode)
render_grid(environment_grid, Qtable)
boat = Boat(environment_grid)
boat.render()
# Reward for Reinforced learning
reward = 0

# Training parameters
training_episodes = 10000


# Evaluation parameters
n_eval_episodes = 100

# Environment parameters
max_steps = 99
eval_seed = []

# Exploration parameters

decay_rate = 0.0005

avg_population = avg_fish_population(environment_grid)
thread = threading.Thread(target=q_learning.train,
                          args=(training_episodes, decay_rate, max_steps, Qtable, tuple(environment_grid), boat, screen, avg_population))
thread.start()


def move_boat(boat, action):
    if action == 0:
        boat.move_up()
    elif action == 1:
        boat.move_down()
    elif action == 2:
        boat.move_left()
    elif action == 3:
        boat.move_right()
    elif action == 4:
        boat.fish()
    else:
        return False
    return True


def printQtable(Qtable):
    for row in Qtable:
        for cell in row:
            print(cell.qvals, end=" ")
        print()


while True:
    render_grid(environment_grid, Qtable)

    if not thread.is_alive():
        print("training over")
        boat.pos = list(boat.reset_pos)
        print(boat.pos)
        """dock = False
        while not dock:
            action = Qtable[boat.pos[0]][boat.pos[1]].qvals.index(max(Qtable[boat.pos[0]][boat.pos[1]].qvals))
            print(action)
            if not move_boat(boat, action):
                dock = True"""

    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    clock.tick(FPS)  # To limit the FPS to 100
    pg.display.flip()
