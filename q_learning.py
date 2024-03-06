import time
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
            return -1
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


def train(training_episodes, min_epsilon, max_epsilon, decay_rate, max_steps, Qtable, environment_grid, boat):

    for episode in range(training_episodes):

        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)
        # Reset the environment
        state = boat.reset_pos
        step = 0
        copy_env_grid = environment_grid.copy()

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

    return Qtable
