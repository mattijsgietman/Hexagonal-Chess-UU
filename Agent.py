import torch as T
import torch.nn.functional as F
import numpy as np
from Replay import ReplayBuffer
from DeepQNetwork import DeepQNetwork

class DQNAgent:
    def __init__(self, gamma, epsilon, lr, input_dims, batch_size, n_actions, max_mem_size=100000, eps_end=0.01, eps_dec=2e-5):
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_min = eps_end
        self.eps_dec = eps_dec
        self.lr = lr
        self.action_space = [i for i in range(n_actions)]
        self.n_actions = n_actions
        self.batch_size = batch_size
        self.mem_size = max_mem_size
        self.replace = 100
        self.learn_step_counter = 0
        self.memory = ReplayBuffer(max_mem_size, input_dims, n_actions)
        
        self.q_eval = DeepQNetwork(lr, n_actions=n_actions, input_dims=input_dims, fc1_dims=256, fc2_dims=128)
        
    def store_transition(self, state, action, reward, state_, done):
        self.memory.store_transition(state, action, reward, state_, done)

    def apply_valid_moves_mask(self, q_values, valid_moves_mask):
        mask_tensor = T.tensor(valid_moves_mask, dtype=T.float).to(self.q_eval.device)
        masked_q_values = q_values * mask_tensor
        return masked_q_values

    def choose_action(self, state, valid_moves_mask):
        state = T.tensor(np.array([state]), dtype=T.float).to(self.q_eval.device)
        actions = self.q_eval.forward(state)
        
        if np.random.random() > self.epsilon:
            masked_actions = self.apply_valid_moves_mask(actions, valid_moves_mask)
            sorted_actions = T.argsort(masked_actions, descending=True).squeeze()
            return sorted_actions.tolist()
        else:
            masked_actions = self.apply_valid_moves_mask(actions, valid_moves_mask)
            max_action_value = masked_actions.max().item()
            if max_action_value == 0:
                return None
            
            valid_indices = np.where(valid_moves_mask == 1)[0]
            if len(valid_indices) == 0:
                return None
            random_move = np.random.choice(valid_indices)
            return [random_move]

    def learn(self):
        if len(self.memory) < self.batch_size:
            return

        self.q_eval.optimizer.zero_grad()

        max_mem = min(len(self.memory), self.mem_size)
        batch = self.memory.sample_buffer(self.batch_size)
        states, actions, rewards, states_, dones = batch

        states = T.tensor(states).to(self.q_eval.device)
        actions = T.tensor(actions).to(self.q_eval.device)
        rewards = T.tensor(rewards).to(self.q_eval.device)
        states_ = T.tensor(states_).to(self.q_eval.device)
        dones = T.tensor(dones).to(self.q_eval.device)

        indices = np.arange(self.batch_size)
        q_pred = self.q_eval.forward(states)[indices, actions]
        q_next = self.q_eval.forward(states_).max(dim=1)[0]
        q_next[dones] = 0.0

        q_target = rewards + self.gamma * q_next

        loss = self.q_eval.loss(q_target, q_pred).to(self.q_eval.device)
        loss.backward()
        self.q_eval.optimizer.step()
        self.epsilon = self.epsilon - self.eps_dec if self.epsilon > self.eps_min else self.eps_min

    def save_models(self):
        T.save(self.q_eval.state_dict(), 'q_eval.pth')

    def load_models(self):
        self.q_eval.load_state_dict(T.load('q_eval.pth'))
