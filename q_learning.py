import time
import pygame as pg
import numpy as np
import random

population_d = 25

# State space -> the simulation grid
# Action space -> all the possible actions
# State -> The current position of the boat in the environment
# Values for action space: up -> 0, down -> 1, left -> 2, right -> 3, fish -> 4 and dock -> 5

def epsilon_greedy_policy(Qtable, state, epsilon):
    random_int = random.uniform(0, 1)
    if random_int > epsilon:
        action = Qtable[state[0]][state[1]].qvals.index(max(Qtable[state[0]][state[1]].qvals))
    else:
        action = random.randint(0,5)
    return action


def take_step(boat, action, environment_grid):
    if action == 0:
        if boat.move_up():
            return -3
        else:
            return -10
    elif action == 1:
        if boat.move_down():
            return -1
        else:
            return -10
    elif action == 2:
        if boat.move_left():
            return -2
        else:
            return -10
    elif action == 3:
        if boat.move_right():
            return -2
        else:
            return -10
    elif action == 4:
        boat.fish()
        fish_population = environment_grid[boat.pos[0]][boat.pos[1]].fish_population
        return fish_population/population_d
    else:
        if boat.dock():
            return 1
        else:
            return -3


learning_rate = 0.7
gamma = 0.95


def render_grid(grid, screen):
    WIDTH = 700
    HEIGHT = 700

    # Variable for the width and the height of the simulation inside the main window
    # Must be <= HEIGHT and WIDTH
    GRID_WIDTH = WIDTH - 200
    GRID_HEIGHT = HEIGHT - 100
    white = (255, 255, 255)
    sea_blue = (50, 152, 168)
    darker_blue = (50, 76, 168)
    x_pos = 0
    y_pos = 0

    no_rows = len(grid)
    no_cols = len(grid[0])
    cell_width = GRID_WIDTH/no_cols
    cell_height = GRID_HEIGHT/no_rows

    for i in range(no_rows):
        for j in range(no_cols):
            rect = cell_width*j, cell_height*i, cell_width, cell_height
            if abs(grid[i][j].fish_population-255) > 255:
                pg.draw.rect(screen, (0, 0, 150), rect)
            else:
                pg.draw.rect(screen, (0, 0, abs(grid[i][j].fish_population-255)), rect)

    for row in grid:
        pg.draw.rect(screen, darker_blue, rect=(0, y_pos, GRID_WIDTH, 1))
        y_pos += cell_height

    for column in grid[0]:
        pg.draw.rect(screen, darker_blue, (x_pos, 0, 1, GRID_HEIGHT))
        x_pos += cell_width


    pg.draw.rect(screen, darker_blue, rect= (0, y_pos, GRID_WIDTH, 1))
    pg.draw.rect(screen, darker_blue, (x_pos, 0, 1, GRID_HEIGHT))

    pg.display.update(pg.Rect(0, 0, GRID_WIDTH+1, GRID_HEIGHT+1))


def train(training_episodes, min_epsilon, max_epsilon, decay_rate, max_steps, Qtable, environment_grid, boat, screen):

    for episode in range(training_episodes):

        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)
        # Reset the environment
        state = list(boat.reset_pos)
        copy_env_grid = list(environment_grid)
        boat.pos = state
        # render_grid(copy_env_grid, screen)
        boat.render()

        step = 0
        print(Qtable)
        # repeat
        for step in range(max_steps):

            action = epsilon_greedy_policy(Qtable, state, epsilon)

            reward = take_step(boat, action, copy_env_grid)
            new_state = boat.pos

            state_val = Qtable[state[0]][state[1]].qvals
            Qtable[state[0]][state[1]].qvals[action] = state_val[action] + learning_rate * (
                        reward + gamma * max(Qtable[new_state[0]][new_state[1]].qvals) - state_val[action])

            if action == 4:
                copy_env_grid[state[0]][state[1]].fish_population -= 100

            # If done, finish the episode
            if action == 5:
                break

            # Our state is the new state
            state = new_state

        #screen.fill((0,0,0))

    return Qtable
