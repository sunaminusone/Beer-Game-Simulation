import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.environment.supply_chain_env import SupplyChainEnvironment
from src.agents.rlom import RLOrderingMechanism
from src.agents.one_for_one import OneForOnePolicy
from src.agents.ga_based import GABasedPolicy
from src.agents.dqn import DQNPolicy
from src.utils.visualizer import (
    plot_inventory,
    plot_orders,
    plot_period_costs,
    plot_total_costs
)
from src.utils.visualizer import plot_cumulative_costs_over_time

def evaluate_strategy(name, policy_class, env_class):
    env = env_class()
    policy = policy_class(env)

    if name == "RLOM":
        print("[Info] Training RLOM strategy...")
        policy.train(episodes=500)

    total_cost, log = policy.evaluate()
    print(f"[{name}] Total Cost: {total_cost}")
    return name, total_cost, log




def main():
    env_class = SupplyChainEnvironment

    results = []

    # Evaluate RLOM
    results.append(evaluate_strategy("RLOM", RLOrderingMechanism, env_class))

    # Evaluate GA-Based
    results.append(evaluate_strategy("GA-Based", GABasedPolicy, env_class))

    # Evaluate One-for-One
    results.append(evaluate_strategy("1-for-1", OneForOnePolicy, env_class))

    # Evaluate DQN
    results.append(evaluate_strategy("DQN", DQNPolicy, env_class))

    # Visualize
    for name, cost, log in results:
        plot_inventory(log, name)
        plot_orders(log, name)
        plot_period_costs(log, name)

   # Optional: summary bar chart of total costs
    plot_total_costs({name: cost for name, cost, _ in results})

    # cumulative cost over time
    plot_cumulative_costs_over_time({
        name: log for name, _, log in results
    })



if __name__ == "__main__":
    main()
