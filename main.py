"""
This file contains the code for the simulation part of the project

The project used pygame for graphics
install using: pip install pygame

Features of the simulation:
1. Map the best fishing path for each day
2. Show the graph of reward vs path per iteration
"""
import json
import pygame as pg
import sys
import random
import q_learning
import threading


# Variables for the width and height of the simulation window
WIDTH = 1100
HEIGHT = 700

# Variable for the width and the height of the simulation inside the main window
# Must be <= HEIGHT and WIDTH
GRID_WIDTH = WIDTH-400
GRID_HEIGHT = HEIGHT
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
        self.qvals = [0, 0, 0, 0, 0]


class OceanEnvironment:
    def __init__(self, row, col, no_row, no_col, mode):
        self.current_row = row
        self.current_col = col

        self.max_rows = no_row-1
        self.max_cols = no_col-1

        self.color = 0

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


    def render(self):
        cell_width = GRID_WIDTH / len(self.grid[0])
        cell_height = GRID_HEIGHT / len(self.grid)
        rect = (cell_width*self.pos[0], cell_height*self.pos[1], cell_width, cell_height)
        pg.draw.rect(screen, white, rect)
        pg.display.update(pg.Rect(rect))


# Creating 2-D array
def create_qtable(rows, columns):
    return [[GridCell() for j in range(columns)] for i in range(rows)]


def create_env(rows, columns, mode):
    return [[OceanEnvironment(i, j, rows, columns, mode) for j in range(columns)] for i in range(rows)]


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
            if grid[i][j].color != 0:
                pg.draw.rect(screen, grid[i][j].color, rect)
            elif (abs(grid[i][j].fish_population-255))>255:
                pg.draw.rect(screen, (0, 0, 255), rect)
            else:
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


def printQtable(Qtable):
    for row in Qtable:
        for cell in row:
            print(cell.qvals, end=" ")
        print()


def save_table(Qtable, file_name):
    saved_table = []
    for row in Qtable:
        for cell in row:
            saved_table.append(cell.qvals)
    with open(file_name, 'w') as file:
        json.dump(saved_table, file)


def save_env(env_grid, file_name):
    saved_table = []
    for row in Qtable:
        for cell in row:
            saved_table.append(cell.qvals)
    with open(file_name, 'w') as file:
        json.dump(saved_table, file)


def load_table(Qtable, file_name):
    with open(file_name, 'r') as file:
        qv = json.load(file)

    ind = 0
    for row in Qtable:
        for cell in row:
            cell.qvals = qv[ind]
            ind += 1


no_rows = 25
no_cols = 25

mode = 1

Qtable = create_qtable(no_rows, no_cols)
environment_grid = create_env(no_rows, no_cols, mode)
#load_table(Qtable, 'save.json')
render_grid(environment_grid, Qtable)
boat = Boat(environment_grid)
boat.render()
# Reward for Reinforced learning
reward = 0

# Training parameters
training_episodes = 500


# Evaluation parameters
n_eval_episodes = 100

# Environment parameters
max_steps = 99
eval_seed = []

# Exploration parameters

decay_rate = 0.0005


def train_model(boat_actor, env_grid):
    avg_population = avg_fish_population(environment_grid)
    thread = threading.Thread(target=q_learning.train,
                              args=(training_episodes, decay_rate, max_steps, Qtable, tuple(env_grid), boat_actor, avg_population))
    thread.start()
    return thread


def update_environment(Qtable, env_grid):
    sm_qvals = 0
    n = 0

    rand_color = (random.randint(0,255), random.randint(0,255), 0)
    for row in Qtable:
        for cell in row:
            qv = cell.qvals
            ind = qv.index(max(qv))
            if ind == 4:
                sm_qvals += qv[4]
                n += 1

    avg = sm_qvals/n
    for row_no, row in enumerate(env_grid):
        for cell_no, cell in enumerate(row):
            qt_cell = Qtable[row_no][cell_no].qvals
            ind = qt_cell.index(max(qt_cell))
            if ind == 4 and qt_cell[ind] > avg*3.5 and cell.color == 0:
                cell.fish_population -= 150
                cell.color = rand_color


saved = False
no_people = 10
no_assigned = 0
running = False

while True:
    render_grid(environment_grid, Qtable)

    if not running and no_assigned<no_people:
        thread = train_model(Boat(Qtable), environment_grid)
        running = True
        no_assigned += 1
    if running and not thread.is_alive():
        update_environment(Qtable, environment_grid)
        Qtable = create_qtable(no_rows, no_cols)
        running = False

    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    clock.tick(FPS)  # To limit the FPS to 100
    pg.display.flip()
