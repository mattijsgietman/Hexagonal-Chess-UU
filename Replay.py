import numpy as np
import random
from collections import deque

from collections import deque
import numpy as np
import random

class ReplayBuffer:
    """
    A replay buffer for storing and sampling transitions for reinforcement learning.

    Parameters:
    - max_size (int): The maximum size of the replay buffer.
    - input_shape (tuple): The shape of the input state.
    - n_actions (int): The number of possible actions.

    Methods:
    - store_transition(state, action, reward, state_, done): Stores a transition in the replay buffer.
    - sample_buffer(batch_size): Samples a batch of transitions from the replay buffer.
    - __len__(): Returns the current size of the replay buffer.
    """

    def __init__(self, max_size, input_shape, n_actions):
        self.memory = deque(maxlen=max_size)
        self.input_shape = input_shape
        self.n_actions = n_actions

    def store_transition(self, state, action, reward, state_, done):
        """
        Stores a transition in the replay buffer.

        Parameters:
        - state: The current state.
        - action: The action taken.
        - reward: The reward received.
        - state_: The next state.
        - done: Whether the episode is done or not.
        """
        transition = (state, action, reward, state_, done)
        self.memory.append(transition)

    def sample_buffer(self, batch_size):
        """
        Samples a batch of transitions from the replay buffer.

        Parameters:
        - batch_size (int): The size of the batch to sample.

        Returns:
        - state: The sampled states.
        - action: The sampled actions.
        - reward: The sampled rewards.
        - new_state: The sampled next states.
        - done: The sampled done flags.
        """
        state, action, reward, new_state, done = zip(*random.sample(self.memory, batch_size))
        return np.array(state), np.array(action), np.array(reward), np.array(new_state), np.array(done)

    def __len__(self):
        """
        Returns the current size of the replay buffer.
        """
        return len(self.memory)
