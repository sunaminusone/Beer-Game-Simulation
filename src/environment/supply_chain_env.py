# We create our Supply Chain Environment of Beer game with 4 levels
class SupplyChainEnvironment:
    def __init__(self, customer_demand=None, lead_times=None, time_horizon=35):
        
        if customer_demand is None:
            # Default customer demand from paper's main test problem
            self.customer_demand = [15, 10, 8, 14, 9, 3, 13, 2, 13, 11, 3, 4, 6, 11, 15, 12, 15, 4, 12, 3, 13, 10, 15, 15, 3, 11, 1, 13, 10,10, 0, 0, 8, 0, 14]                 
        else:
            self.customer_demand = customer_demand
            
        
        if lead_times is None:
            # Default lead times from paper's main test problem
            self.lead_times = [2, 0, 2, 4, 4, 4, 0, 2, 4, 1, 1, 0, 0, 1, 1, 0, 1, 1, 2, 1, 1, 1, 4, 2, 2, 1, 4, 3, 4, 1, 4, 0, 3, 3, 4]
        else:
            self.lead_times = lead_times
            
        self.time_horizon = time_horizon
        
        # Initial inventories:
        self.inventory_position = [12, 12, 12, 12]  # [retailer, distributor, manufacturer, supplier]
        self.pipeline = [[[4, 1], [4, 2]] for _ in range(4)]  # [amount, time_remaining]
        
        # Current time step
        self.current_time = 0
        
        # Cost parameters
        self.holding_cost = 1  # $1 per unit per period
        self.backlog_cost = 2  # $2 per unit per period
        
        # Track orders received by each actor at each time step
        self.orders_received = [0, 0, 0, 0]  # [retailer, distributor, manufacturer, supplier]
        
        # Track costs
        self.period_costs = []
        self.total_cost = 0

        self.inventory_history = [[] for _ in range(4)]
        self.order_history = [[] for _ in range(4)]

        
    def code_state(self, state):
        coded_state = []
        for inventory in state:
            if inventory < -6:
                coded_state.append(1)
            elif inventory < -3:
                coded_state.append(2)
            elif inventory < 0:
                coded_state.append(3)
            elif inventory < 3:
                coded_state.append(4)
            elif inventory < 6:
                coded_state.append(5)
            elif inventory < 10:
                coded_state.append(6)
            elif inventory < 15:
                coded_state.append(7)
            elif inventory < 20:
                coded_state.append(8)
            else:
                coded_state.append(9)
        return tuple(coded_state)
    
    def get_state(self):
        return self.inventory_position.copy()
    
    def get_coded_state(self):
        return self.code_state(self.inventory_position)
    
    def calculate_cost(self):
        cost = 0
        for inventory in self.inventory_position:
            if inventory > 0:
                cost += self.holding_cost * inventory  # Holding cost
            else:
                cost += self.backlog_cost * abs(inventory)  # Backlog cost
        return cost
    
    def step(self, actions):
        if self.current_time >= self.time_horizon:
            return self.get_state(), 0, True, {}

        customer_demand = self.customer_demand[self.current_time]
        lead_time = self.lead_times[self.current_time]

        # Process incoming goods
        for i in range(4):
            for package in self.pipeline[i]:
                if package[1] > 0:
                    package[1] -= 1

            delivered = sum(package[0] for package in self.pipeline[i] if package[1] == 0)
            self.inventory_position[i] += delivered
            self.pipeline[i] = [package for package in self.pipeline[i] if package[1] > 0]

        # Process orders from downstream
        self.orders_received[0] = customer_demand

        for i in range(4):
            order = customer_demand if i == 0 else self.orders_received[i]

            if self.inventory_position[i] >= order:
                self.inventory_position[i] -= order
                if i > 0:
                    self.pipeline[i - 1].append([order, lead_time])
            else:
                available = max(0, self.inventory_position[i])
                backordered = order - available

                if available > 0:
                    self.inventory_position[i] -= available
                    if i > 0:
                        self.pipeline[i - 1].append([available, lead_time])

                self.inventory_position[i] -= backordered

        # Place upstream orders
        for i in range(4):
            if i == 0:
                order_size = customer_demand + actions[i]
                self.orders_received[1] = order_size
            elif i < 3:
                order_size = self.orders_received[i] + actions[i]
                self.orders_received[i + 1] = order_size
            else:
                order_size = self.orders_received[i] + actions[i]
                self.pipeline[i].append([order_size, lead_time])

        cost = self.calculate_cost()
        self.period_costs.append(cost)
        self.total_cost += cost
        self.current_time += 1

        for i in range(4):
            self.inventory_history[i].append(self.inventory_position[i])
            self.order_history[i].append(self.orders_received[i])

        return self.get_state(), -cost, self.current_time >= self.time_horizon, {"period_cost": cost}

    
    def reset(self):
        # Initialize supply chain for reset
        self.inventory_position = [12, 12, 12, 12]  
        self.pipeline = [[[4, 1], [4, 2]] for _ in range(4)]  
        
        # Reset time step
        self.current_time = 0
        
        # Reset tracking variables
        self.orders_received = [0, 0, 0, 0]
        self.period_costs = []
        self.total_cost = 0
        
        return self.get_state()