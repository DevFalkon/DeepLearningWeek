"""
This file contains the code for the simulation part of the project

The project used pygame for graphics
install using: pip install pygame

Features of the simulation:
1. Map the best fishing path for each day
2. Show the graph of reward vs path per iteration
"""
import random

import pygame as pg
import sys
import numpy as np
import random


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
        self.fish_population = random.randint(0, 255)
        self.environment_val = 0

        self.population_history = []


# All the properties of the boat
class Boat:
    def __init__(self, grid):
        # position is the grid coordinates of the boat
        self.pos = [0, len(grid)-1]

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
        if self.pos[0] < len(self.grid)-1:
            self.pos[0] -= 1
            self.render()
            return True
        return False

    def move_right(self):
        if self.pos[0] > 0:
            self.pos[0] += 1
            self.render()
            return True
        return False

    def fish(self):
        decline = 10
        self.grid[self.pos[0]][self.pos[1]].fish_population -= decline

    def dock(self):
        if self.pos[1] == len(self.grid[0])-1:
            return True
        return False

    def render(self):
        cell_width = GRID_WIDTH / len(self.grid[0])
        cell_height = GRID_HEIGHT / len(self.grid)
        rect = (cell_width*self.pos[0], cell_height*self.pos[1], cell_width, cell_height)
        pg.draw.rect(screen, white, rect)
        pg.display.update(pg.Rect(rect))


# Creating an empty 2-D array
def create_grid(rows, columns):
    ls = [[GridCell() for j in range(columns)] for i in range(rows)]
    return ls


# Rendering the grid on screen
def render_grid(grid):
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
state_grid = create_grid(no_rows, no_cols)
render_grid(state_grid)
boat = Boat(state_grid)
boat.render()
# Reward for Reinforced learning
reward = 0

while True:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    clock.tick(FPS)  # To limit the FPS to 100
    pg.display.flip()
