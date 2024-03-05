import numpy as np
import random

# Training parameters
n_training_episodes = 10000
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

# Values for Q-table: up -> 0, down -> 1, left -> 2, right -> 3, fish -> 4 and dock -> 5
def initialize_q_table(state_space, action_space):
  Qtable = np.zeros((state_space, action_space))
  return Qtable


def epsilon_greedy_policy(Qtable, state, epsilon):
  random_int = random.uniform(0,1)
  if random_int > epsilon:
    action = np.argmax(Qtable[state])
  else:
    action = env.action_space.sample()
  return action


def train(n_training_episodes, min_epsilon, max_epsilon, decay_rate, grid, max_steps, Qtable):
    for episode in trange(n_training_episodes):

        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)
        # Reset the environment
        state = env.reset()
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
