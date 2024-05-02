from DeepQNetwork import DeepQNetwork
import numpy as np

class Agent():
    def __init__(self, gamma, epsilon, lr, input_dims, batch_size, n_actions,
                 max_mem_size=100000, eps_end=0.01, eps_dec=5e-4):
        self.gamma = gamma
        self.epsilon = epsilon
        self.lr = lr
        self.input_dims = input_dims
        self.batch_size = batch_size
        self.n_actions = n_actions
        self.max_mem_size = max_mem_size
        self.eps_end = eps_end
        self.eps_dec = eps_dec
        self.action_space = [i for i in range(n_actions)]
        self.mem_size = 0

        self.Q_eval = DeepQNetwork(self.lr, input_dims=self.input_dims, 
                                   n_actions=self.n_actions, fc1_dims=256, fc2_dims=256)

        self.state_memory = np.zeros((self.max_mem_size, *input_dims), dtype=np.float32)
        self.new_state_memory = np.zeros((self.max_mem_size, *input_dims), 
                                         dtype=np.float32)
        self.action_memory = np.zeros(self.max_mem_size, dtype=np.float32)
        self.reward_memory = np.zeros(self.max_mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.max_mem_size, dtype=np.bool)
        
    def store_transition(self, state, action, reward, state_, done):
        index = self.mem_size % self.max_mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        self.reward_memory[index] = reward
        self.action_memory[index] = action
        self.terminal_memory[index] = done

        self.mem_size += 1
