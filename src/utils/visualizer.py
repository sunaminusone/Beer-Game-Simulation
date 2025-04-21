import plotly.graph_objs as go
import plotly.express as px
import os

def plot_inventory(env_log, strategy_name):
    time_steps = list(range(len(env_log["inventory_history"][0])))
    labels = ['Retailer', 'Distributor', 'Manufacturer', 'Supplier']
    colors = px.colors.qualitative.Pastel  # Macaron color palette

    fig = go.Figure()
    for i in range(4):
        fig.add_trace(go.Scatter(
            x=time_steps,
            y=env_log["inventory_history"][i],
            mode='lines',
            name=labels[i],
            line=dict(width=3, color=colors[i % len(colors)])
        ))

    fig.update_layout(
        title=f"\U0001F4E6 Inventory Over Time — {strategy_name}",
        xaxis_title="Time Step",
        yaxis_title="Inventory Level",
        template="plotly_white",
        font=dict(size=14),
        legend=dict(title="Supply Chain Level"),
    )

    fig.write_html(f"results/{strategy_name.lower()}_inventory.html")
    return fig

def plot_orders(env_log, strategy_name):
    time_steps = list(range(len(env_log["order_history"][0])))
    labels = ['Retailer', 'Distributor', 'Manufacturer', 'Supplier']
    colors = px.colors.qualitative.Pastel

    fig = go.Figure()
    for i in range(4):
        fig.add_trace(go.Scatter(
            x=time_steps,
            y=env_log["order_history"][i],
            mode='lines',
            name=labels[i],
            line=dict(width=3, color=colors[i % len(colors)])
        ))

    fig.update_layout(
        title=f"\U0001F4E6 Orders Over Time — {strategy_name}",
        xaxis_title="Time Step",
        yaxis_title="Order Quantity",
        template="plotly_white",
        font=dict(size=14),
        legend=dict(title="Supply Chain Level"),
    )

    fig.write_html(f"results/{strategy_name.lower()}_orders.html")
    return fig

def plot_period_costs(env_log, strategy_name):
    time_steps = list(range(len(env_log["period_costs"])))
    colors = px.colors.qualitative.Pastel

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=time_steps,
        y=env_log["period_costs"],
        marker_color=colors[2]
    ))

    fig.update_layout(
        title=f"\U0001F4B0 Period Costs Over Time — {strategy_name}",
        xaxis_title="Time Step",
        yaxis_title="Cost",
        template="plotly_white",
        font=dict(size=14),
    )

    fig.write_html(f"results/{strategy_name.lower()}_costs.html")
    return fig

def plot_total_costs(strategy_costs_dict):
    names = list(strategy_costs_dict.keys())
    costs = list(strategy_costs_dict.values())
    colors = px.colors.qualitative.Pastel

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=names,
        y=costs,
        marker_color=colors[:len(names)]
    ))

    fig.update_layout(
        title="\U0001F4CA Total Cost Comparison Across Strategies",
        xaxis_title="Strategy",
        yaxis_title="Total Cost",
        template="plotly_white",
        font=dict(size=14),
    )

    fig.write_html("results/total_costs_comparison.html")
    return fig

def plot_cumulative_costs_over_time(strategies_results_dict):
    """
    Plots a line chart of accumulated cost over time for each strategy.
    """
    colors = px.colors.qualitative.Pastel
    fig = go.Figure()

    for i, (name, env_log) in enumerate(strategies_results_dict.items()):
        costs = env_log["period_costs"]
        print(f"[DEBUG] {name} → period_costs length: {len(costs)}") 
        accumulated_cost = []
        running_total = 0
        for cost in costs:
            try:
                cost = float(cost)
                running_total += cost
                accumulated_cost.append(running_total)
            except (ValueError, TypeError):
                continue

        if accumulated_cost:
            fig.add_trace(go.Scatter(
                x=list(range(len(accumulated_cost))),
                y=accumulated_cost,
                mode='lines+markers',
                name=f"{name} (Total: {int(accumulated_cost[-1])})",
                line=dict(width=3, color=colors[i % len(colors)])
            ))

    fig.update_layout(
        title="\U0001F4C8 Accumulated Cost Over Time by Strategy",
        xaxis_title="Time Step",
        yaxis_title="Accumulated Cost",
        template="plotly_white",
        font=dict(size=14)
    )

    fig.write_html("results/cumulative_costs_over_time.html")
    return fig
