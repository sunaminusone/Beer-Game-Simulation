class OneForOnePolicy:
    def __init__(self, env):
        self.env = env

    def evaluate(self):
        """
        Evaluates the classic 1-for-1 policy (order = demand) in the Beer Game environment.
        Returns total cost and a log dictionary containing inventory, orders, and period costs.
        """
        state = self.env.reset()
        total_reward = 0
        done = False

        # Initialize logging structures
        inventory_history = [[], [], [], []]
        order_history = [[], [], [], []]
        period_costs = []

        while not done:
            # 1-for-1 policy: order exactly what was received from downstream
            actions = [self.env.orders_received[i] for i in range(4)]
            next_state, reward, done, info = self.env.step(actions)

            # Log inventory and orders for each level
            for i in range(4):
                inventory_history[i].append(self.env.inventory_position[i])
                order_history[i].append(self.env.orders_received[i])

            period_costs.append(info["period_cost"])
            total_reward += reward
            state = next_state

        log = {
            "inventory_history": inventory_history,
            "order_history": order_history,
            "period_costs": period_costs
        }

        return -total_reward, log  # Return total cost and log
