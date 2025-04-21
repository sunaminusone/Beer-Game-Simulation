# simplified GA-based policy from the paper
class GABasedPolicy:
    def __init__(self, env):
        self.env = env
        
        # Fixed Y values for each actor based on approximate GA solution from the paper
        self.fixed_y_values = [1, 2, 1, 0] 
    
    def evaluate(self):
        """
        Evaluates the GA-based fixed strategy in the environment.
        Returns total cost and time-series log data for plotting.
        """
        state = self.env.reset()
        total_reward = 0
        done = False

        # Initialize logging structures
        inventory_history = [[], [], [], []]
        order_history = [[], [], [], []]
        period_costs = []

        while not done:
            action = self.fixed_y_values  # Use fixed Y values for all steps
            next_state, reward, done, info = self.env.step(action)

            # Log inventory and order data for each level
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

        return -total_reward, log  # Return positive cost and log dictionary


