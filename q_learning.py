import numpy as np
import random

# Training parameters
training_episodes = 10000
learning_rate = 0.7

# Evaluation parameters
n_eval_episodes = 100

# Environment parameters
max_steps = 99
gamma = 0.95
eval_seed = []

# Exploration parameters
max_epsilon = 1.0
min_epsilon = 0.05
decay_rate = 0.0005

# State space -> the simulation grid
# Action space -> all the possible actions
# State -> The current position of the boat in the environment
# Values for action space: up -> 0, down -> 1, left -> 2, right -> 3, fish -> 4 and dock -> 5

def epsilon_greedy_policy(Qtable, state, epsilon):
    random_int = random.uniform(0, 1)
    if random_int > epsilon:
        action = max(Qtable[state[0]][state[1]].qvals)
    else:
        action = Qtable[state[0]][state[1]].q_values[random.randint(0,6)]
    return action


def reset():
    pass


def take_step(boat, action):
    if action == 0:
        boat.move_up()
    elif action == 1:
        boat.move_down()
    elif action == 2:
        boat.move_left()
    elif action == 3:
        boat.move_down()
    elif action == 4:
        boat.fish()
    else:
        boat.dock()


def train(training_episodes, min_epsilon, max_epsilon, decay_rate, max_steps, Qtable, boat):
    for episode in range(training_episodes):

        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)
        # Reset the environment
        state = boat.reset_pos
        step = 0
        done = False

        # repeat
        for step in range(max_steps):

            action = epsilon_greedy_policy(Qtable, state, epsilon)

            new_state, reward, done, info = env.step(action)

            Qtable[state][action] = Qtable[state][action] + learning_rate * (
                        reward + gamma * np.max(Qtable[new_state]) - Qtable[state][action])

            # If done, finish the episode
            if done:
                break

            # Our state is the new state
            state = new_state
    return Qtable
