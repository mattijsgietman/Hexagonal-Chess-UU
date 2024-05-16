import numpy as np
import random
from collections import deque

class ReplayBuffer:
    def __init__(self, max_size, input_shape, n_actions):
        self.memory = deque(maxlen=max_size)
        self.input_shape = input_shape
        self.n_actions = n_actions

    def store_transition(self, state, action, reward, state_, done):
        transition = (state, action, reward, state_, done)
        self.memory.append(transition)

    def sample_buffer(self, batch_size):
        state, action, reward, new_state, done = zip(*random.sample(self.memory, batch_size))
        return np.array(state), np.array(action), np.array(reward), np.array(new_state), np.array(done)

    def __len__(self):
        return len(self.memory)
