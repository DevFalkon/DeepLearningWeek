import time
import pygame as pg
import numpy as np
import random

population_d = 70

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


def take_step(boat, action, environment_grid, avg_population):
    if action == 0:
        if boat.move_up():
            return -5
        return -100
    elif action == 1:
        if boat.move_down():
            return -1
        return -100
    elif action == 2:
        if boat.move_left():
            return -1.5
        return -100
    elif action == 3:
        if boat.move_right():
            return -1.5
        return -100
    elif action == 4:
        fish_population = environment_grid[boat.pos[1]][boat.pos[0]].fish_population
        if fish_population < avg_population:
            return -1*fish_population/population_d
        return fish_population/population_d
    else:
        if boat.dock():
            return -1
        else:
            return -100


learning_rate = 0.7
gamma = 0.95


import copy


def train(training_episodes, decay_rate, max_steps, Qtable, environment_grid, boat, screen, avg_population):

    max_epsilon = 1.0
    min_epsilon = 0.05

    for episode in range(training_episodes):

        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)
        # Reset the environment
        state = list(boat.reset_pos)
        copy_env_grid = copy.deepcopy(list(environment_grid))
        boat.pos = state

        # repeat
        for step in range(max_steps):

            action = epsilon_greedy_policy(Qtable, state, epsilon)

            reward = take_step(boat, action, copy_env_grid, avg_population)
            new_state = boat.pos

            state_val = Qtable[state[1]][state[0]].qvals
            Qtable[state[1]][state[0]].qvals[action] = state_val[action] + learning_rate * (
                        reward + gamma * max(Qtable[new_state[1]][new_state[0]].qvals) - state_val[action])

            if action == 4:
                copy_env_grid[state[1]][state[0]].fish_population -= 100

            # If done, finish the episode
            if action == 5:
                break

            # Our state is the new state
            state = new_state

    return Qtable
