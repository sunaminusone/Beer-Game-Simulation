# Beer Game Simulation

This project implements a simulation of the classic **Beer Game**, a supply chain management exercise that explores the dynamics of inventory control across four echelons: Retailer, Wholesaler, Distributor, and Factory.

We simulate and evaluate different ordering policies to analyze their impact on total supply chain cost and dynamics.

## 📌 Implemented Strategies

1. **One-for-One Policy**  
   A basic rule-based policy where each agent orders exactly the amount it received from its downstream partner in the previous period.

2. **GA-Based Policy**  
   A fixed ordering policy derived from approximate solutions using Genetic Algorithms (based on academic literature).

3. **RLOM: Reinforcement Learning Ordering Mechanism**  
   A Q-learning based policy that learns to minimize total cost over multiple episodes using tabular Q-learning.

4. **DQN (Deep Q-Network)**  
   A neural network-based RL policy to handle larger state/action spaces and improve generalization.

## 🛠 File Structure (currently)

- `SCM_using_RLOM.ipynb`: Jupyter notebook implementing the environment and the three policies above.

## 🚀 Getting Started

1. Clone the repository:

```bash
git clone https://github.com/haeminusone/Beer-Game-Simulation.git
cd Beer-Game-Simulation
