import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random

class QNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(QNetwork, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim)
        )

    def forward(self, x):
        return self.model(x)


class DQNPolicy:
    def __init__(self, env, state_dim=4, action_dim=256, gamma=0.99, lr=0.001, epsilon=1.0):
        self.env = env
        self.model = QNetwork(state_dim, action_dim)
        self.target_model = QNetwork(state_dim, action_dim)
        self.target_model.load_state_dict(self.model.state_dict())
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.memory = deque(maxlen=10000)
        self.gamma = gamma
        self.epsilon = epsilon
        self.batch_size = 64

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return random.randint(0, 255)
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state)
            q_values = self.model(state_tensor)
            return torch.argmax(q_values).item()

    def evaluate(self):
        # simplified evaluation using fixed policy
        state = self.env.reset()
        done = False
        total_reward = 0
        inventory_history = [[] for _ in range(4)]
        order_history = [[] for _ in range(4)]
        period_costs = []

        while not done:
            state_code = self.env.code_state(state)
            action = [0, 0, 0, 0]  # Replace with proper decoding logic
            next_state, reward, done, info = self.env.step(action)

            for i in range(4):
                inventory_history[i].append(self.env.inventory_position[i])
                order_history[i].append(self.env.orders_received[i])

            period_costs.append(info["period_cost"])
            state = next_state
            total_reward += reward

        log = {
            "inventory_history": inventory_history,
            "order_history": order_history,
            "period_costs": period_costs
        }

        return -total_reward, log
