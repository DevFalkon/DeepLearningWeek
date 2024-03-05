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
import numpy as np


# Variables for the width and height of the simulation window
WIDTH = 700
HEIGHT = 700

# Variable for the width and the height of the simulation inside the main window
# Must be <= HEIGHT and WIDTH
GRID_WIDTH = WIDTH-200
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
        self.fish_population = 0
        self.environment_val = 0

        self.population_history = []


# All the properties of the boat
class Boat:
    def __init__(self):
        # position is the grid coordinates of the boat
        self.pos = (0,0)
        self.fuel_used = 0

    def move_up(self):
        pass

    def move_down(self):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass

    def fish(self):
        pass


# Creating an empty 2-D array
def create_grid(rows, columns):
    ls = [[GridCell for j in range(columns)] for i in range(rows)]
    return ls


# Rendering the grid on screen
def render_grid(grid):
    x_pos = 0
    y_pos = 0

    x_increment = GRID_WIDTH/len(grid[0])
    y_increment = GRID_HEIGHT/len(grid)

    for row in grid:
        pg.draw.rect(screen, darker_blue, rect=(0, y_pos, GRID_WIDTH, 1))
        y_pos += y_increment

    for column in grid[0]:
        pg.draw.rect((screen), darker_blue, (x_pos, 0, 1, GRID_HEIGHT))
        x_pos += x_increment

    pg.draw.rect(screen, darker_blue, rect=(0, y_pos, GRID_WIDTH, 1))
    pg.draw.rect(screen, darker_blue, (x_pos, 0, 1, GRID_HEIGHT))

    pg.display.update(pg.Rect(0, 0, GRID_WIDTH+1, GRID_HEIGHT+1))


no_rows = 25
no_cols = 25
grid_state = create_grid(no_rows, no_cols)
render_grid(grid_state)

# Reward for Reinforced learning
reward = 0

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    clock.tick(FPS)  # To limit the FPS to 100
