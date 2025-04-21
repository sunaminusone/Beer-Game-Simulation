# Reinforcement Learning Ordering Mechanism for supply chain management
import pandas as np
import numpy as np
from collections import defaultdict


class RLOrderingMechanism:
    def __init__(self, env, learning_rate=0.17, discount_factor=1.0, action_range=4):
        
        self.env = env
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.action_range = action_range
        
        # Initialize Q-table 
        self.q_table = defaultdict(lambda: np.zeros((action_range, action_range, action_range, action_range)))
        
        self.episode_rewards = []
        
    def choose_action(self, state, exploration_prob):
        coded_state = self.env.code_state(state)
        
        if np.random.random() < exploration_prob:
            return [np.random.randint(0, self.action_range) for _ in range(4)]
        else:
            # choose the best action based on Q-values
            q_values = self.q_table[coded_state]
            best_action_index = np.unravel_index(np.argmax(q_values), q_values.shape)
            return list(best_action_index)
    
    def update_q_table(self, state, action, reward, next_state):
        coded_state = self.env.code_state(state)
        coded_next_state = self.env.code_state(next_state)
        
        # Get current Q-value
        current_q = self.q_table[coded_state][tuple(action)]
        
        next_max_q = np.max(self.q_table[coded_next_state])
        
        # Update Q-value using Q-learning formula
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        
        self.q_table[coded_state][tuple(action)] = new_q

    
    def train(self, episodes=500, max_steps=35, initial_exploration=0.98, final_exploration=0.1):
        for episode in range(episodes):
            # Reset environment
            state = self.env.reset()
            total_reward = 0
            done = False
            
            exploration_prob = initial_exploration - episode * (initial_exploration - final_exploration) / episodes
            
            for step in range(max_steps):
                if done:
                    break
                
                # Adjust exploration probability within episode 
                step_exploration = exploration_prob - step * (exploration_prob - 0.02) / max_steps
                action = self.choose_action(state, step_exploration)
                next_state, reward, done, _ = self.env.step(action)
                
                self.update_q_table(state, action, reward, next_state)
                
                state = next_state
                total_reward += reward
            
            self.episode_rewards.append(total_reward)
            
            # Print every 50 episodes
            if (episode + 1) % 50 == 0:
                print(f"Episode: {episode + 1}/{episodes}, Total Reward: {total_reward}, Total Cost: {-total_reward}")
        
        return self.episode_rewards
    
    def get_optimal_policy(self):
        policy = {}
        for coded_state in self.q_table:
            q_values = self.q_table[coded_state]
            best_action_index = np.unravel_index(np.argmax(q_values), q_values.shape)
            policy[coded_state] = list(best_action_index)
        return policy
    
    def evaluate_policy(self, policy=None):
        # Reset environment
        state = self.env.reset()
        total_reward = 0
        done = False
        period_costs = []
        
        while not done:
            if policy is None:
                coded_state = self.env.code_state(state)
                action = self.get_optimal_policy().get(coded_state, [0, 0, 0, 0])
            else:
                coded_state = self.env.code_state(state)
                action = policy.get(coded_state, [0, 0, 0, 0])
            
            next_state, reward, done, info = self.env.step(action)
            
            state = next_state
            total_reward += reward
            period_costs.append(info["period_cost"])
        
        return -total_reward, period_costs
    
    def evaluate(self):
        state = self.env.reset()
        total_reward = 0
        done = False

        # Initialize logging structures
        inventory_history = [[], [], [], []]
        order_history = [[], [], [], []]
        period_costs = []

        # Get optimal action policy from Q-table
        optimal_policy = self.get_optimal_policy()

        while not done:
            # Determine action from policy
            coded_state = self.env.code_state(state)
            action = optimal_policy.get(coded_state, [0, 0, 0, 0])  # fallback: no adjustment

            # Environment step
            next_state, reward, done, info = self.env.step(action)

            # Log inventory and order data for each level
            for i in range(4):
                inventory_history[i].append(self.env.inventory_position[i])
                order_history[i].append(self.env.orders_received[i])

            # Log cost for this period
            period_costs.append(info["period_cost"])

            # Advance to next state
            state = next_state
            total_reward += reward

        # Package log for visualization
        log = {
            "inventory_history": inventory_history,
            "order_history": order_history,
            "period_costs": period_costs
        }

        return -total_reward, log  # Return total cost (positive value) and log
