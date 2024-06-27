import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

class DeepQNetwork(nn.Module):
    """
    Deep Q-Network class for reinforcement learning.

    Args:
        lr (float): Learning rate for the optimizer.
        input_dims (tuple): Dimensions of the input state.
        fc1_dims (int): Number of units in the first fully connected layer.
        fc2_dims (int): Number of units in the second fully connected layer.
        n_actions (int): Number of possible actions.

    Attributes:
        lr (float): Learning rate for the optimizer.
        input_dims (tuple): Dimensions of the input state.
        fc1_dims (int): Number of units in the first fully connected layer.
        fc2_dims (int): Number of units in the second fully connected layer.
        n_actions (int): Number of possible actions.
        fc1 (nn.Linear): First fully connected layer.
        fc2 (nn.Linear): Second fully connected layer.
        fc3 (nn.Linear): Third fully connected layer.
        optimizer (torch.optim.Adam): Optimizer for updating the model parameters.
        loss (nn.MSELoss): Loss function for training the model.
        device (torch.device): Device (CPU or GPU) on which the model is located.

    Methods:
        forward(state): Performs a forward pass through the network.

    """

    def __init__(self, lr, input_dims, fc1_dims, fc2_dims, n_actions):
        super(DeepQNetwork, self).__init__()
        self.lr = lr
        self.input_dims = input_dims
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims
        self.n_actions = n_actions

        self.fc1 = nn.Linear(*self.input_dims, self.fc1_dims)
        self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)
        self.fc3 = nn.Linear(self.fc2_dims, self.n_actions)

        self.optimizer = optim.Adam(self.parameters(), lr=self.lr)
        self.loss = nn.MSELoss()

        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, state):
        """
        Performs a forward pass through the network.

        Args:
            state (torch.Tensor): Input state.

        Returns:
            torch.Tensor: Output actions.

        """
        state = state.float()
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        actions = self.fc3(x)

        return actions
