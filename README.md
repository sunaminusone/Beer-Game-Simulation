## Beer Game Simulation

This project simulates the classic **Beer Game**, a multi-tier supply chain environment, and compares different inventory control strategies in terms of cost and performance.

The Beer Game involves four agents — **Retailer**, **Wholesaler**, **Distributor**, and **Factory** — all trying to fulfill customer demand with limited information and time delays. The goal is to manage inventory efficiently and minimize total supply chain cost.

---

## 📌 Implemented Strategies

- **One-for-One Policy**  
  A simple rule-based strategy where each agent orders exactly the amount it received from its downstream partner.

- **GA-Based Policy**  
  A fixed ordering strategy derived from approximate solutions using Genetic Algorithms.

- **RLOM (Reinforcement Learning Ordering Mechanism)**  
  A tabular Q-learning based policy that learns optimal ordering decisions from interaction with the environment.

- **DQN (Deep Q-Network)**  
  A deep reinforcement learning agent that uses neural networks to approximate Q-values for scalable decision-making.

---

## 🛠 Project Structure

```
beer-game-simulation/
├── LICENSE                     # MIT License
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── src/
│   ├── environment/
│   │   └── supply_chain_env.py     # Core Beer Game environment
│   ├── agents/                     # Agent implementations
│   │   ├── one_for_one.py
│   │   ├── ga_based.py
│   │   ├── rlom.py
│   │   └── dqn.py
│   └── utils/
│       └── visualizer.py          # Visualization helper functions
├── experiments/
│   └── compare_policies.py        # Script for running simulations
├── notebooks/
│   └── SCM_using_RLOM.ipynb       # Jupyter notebook for prototyping
└── results/
    └── .gitkeep                   # Placeholder for output files
```

---

## 🚀 Getting Started

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/beer-game-simulation.git
cd beer-game-simulation
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the experiment:**

```bash
python experiments/compare_policies.py
```

4. *(Optional)* Launch the notebook:

```bash
jupyter notebook notebooks/SCM_using_RLOM.ipynb
```

---

## 📦 Requirements

Minimal dependencies:

```
numpy
matplotlib
```

If you're using the DQN strategy, additional requirements may include:

```
torch
gym
```

These can be added in `requirements.txt`.

---

## 📈 Future Improvements

- Add interactive visualization for inventory and orders
- Tune DQN hyperparameters and architecture
- Implement multi-agent reinforcement learning (MARL)
- Dockerize for reproducibility

---

## 📄 License

This project is licensed under the terms of the [MIT License](./LICENSE).

---

## 🤝 Contributions

Contributions are welcome! Please feel free to open issues or submit pull requests.

---
```

