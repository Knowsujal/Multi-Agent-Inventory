import sys
import os
import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulate_agent_comm import simulate_day
from planner_agent import PlannerAgent
from store_agent import StoreAgent
from warehouse_agent import WarehouseAgent
import pandas as pd

# Create output directories if they don't exist
os.makedirs("visualizations", exist_ok=True)
os.makedirs("docs/visualizations", exist_ok=True)

def main():
    # Sample product IDs from each dataset (non-overlapping)
    demand_product_id = 1001
    inventory_product_id = 9286
    pricing_product_id = 9502

    print("=" * 60)
    print(f"[Main] Starting Inventory Optimization")
    print("=" * 60)

    planner = PlannerAgent("demand_forecasting.csv")
    inventory_data = pd.read_csv("inventory_monitoring.csv")
    pricing_data = pd.read_csv("pricing_optimization.csv")

    if planner.data is None:
        print(f"[Main] Error: Could not load forecasting data. Exiting.")
        return

    forecast = planner.get_demand_forecast(demand_product_id)
    if forecast is None or forecast <= 0:
        print(f"[Main] Forecast unavailable or invalid for Product ID: {demand_product_id}. Exiting.")
        return

    inventory_row = inventory_data[inventory_data['Product ID'] == inventory_product_id]
    if inventory_row.empty:
        print(f"[Main] Inventory data not found for Product ID {inventory_product_id}.")
        return

    current_stock = int(inventory_row['Stock Levels'].values[0])
    reorder_point = int(inventory_row['Reorder Point'].values[0])
    lead_time = int(inventory_row['Supplier Lead Time (days)'].values[0])

    store = StoreAgent(product_id=inventory_product_id, current_stock=current_stock, lead_time_days=lead_time, reorder_point=reorder_point)
    warehouse = WarehouseAgent()
    warehouse.set_stock(product_id=inventory_product_id, quantity=500)
    store.evaluate_and_order(forecast, warehouse)

    price_row = pricing_data[pricing_data['Product ID'] == pricing_product_id]
    if price_row.empty:
        print(f"[Main] Pricing data not found for Product ID {pricing_product_id}.")
        return

    elasticity = float(price_row['Elasticity Index'].values[0])
    competitor_price = float(price_row['Competitor Prices'].values[0])
    base_price = float(price_row['Price'].values[0])
    optimal_price = round(base_price * (1 + (1 - elasticity) * 0.1), 2)

    simulation_days = 7
    start_date = datetime.today()
    product_ids = inventory_data['Product ID'].unique()[:3]

    report_data = []
    for day in range(simulation_days):
        current_date = start_date + timedelta(days=day)
        fig, axs = plt.subplots(len(product_ids), 1, figsize=(10, 5 * len(product_ids)))
        if len(product_ids) == 1:
            axs = [axs]

        for i, pid in enumerate(product_ids):
            forecast = planner.get_demand_forecast(pid)
            current_stock = warehouse.get_stock(pid)
            reorder_point = forecast * 1.2
            lead_time = 5 + day % 3
            price = max(1, round(optimal_price, 2))

            if day > 0 and report_data[-len(product_ids)]['Units Fulfilled'] > forecast:
                price *= 1.05
            elif day > 0 and report_data[-len(product_ids)]['Units Fulfilled'] < forecast:
                price *= 0.95

            ordered_qty = forecast + (forecast * 0.3)
            fulfilled = min(ordered_qty, current_stock)
            warehouse.set_stock(pid, current_stock - fulfilled)

            report_data.append({
                "Date": current_date.date(),
                "Product ID": pid,
                "Forecasted Demand": round(forecast, 2),
                "Price": round(price, 2),
                "Stock Before": current_stock,
                "Units Fulfilled": round(fulfilled, 2),
                "Stock After": round(current_stock - fulfilled, 2)
            })

            axs[i].bar(["Forecast", "Fulfilled"], [forecast, fulfilled], color=['skyblue', 'green'])
            axs[i].set_title(f"Product {pid} - Day {day + 1}")
            axs[i].set_ylabel("Units")
            axs[i].set_ylim(0, max(forecast, fulfilled) * 1.5)

        plt.tight_layout()
        filename = f"day_{day + 1}.png"
        plt.savefig(f"docs/visualizations/{filename}")
        plt.close()

    with open('docs/simulation_report.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=report_data[0].keys())
        writer.writeheader()
        writer.writerows(report_data)

    generate_html()
    print("\n✅ Simulation complete. Report and visuals are ready in the docs/ folder.")

def generate_html():
    visual_folder = "docs/visualizations"
    output_html_path = "docs/index.html"
    images = sorted([f for f in os.listdir(visual_folder) if f.endswith(".png")])

    html = """
<!DOCTYPE html>
<html>
<head>
  <title>Multi-Agent Inventory Visuals</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 20px; }
    img { max-width: 90%; margin-bottom: 20px; border: 1px solid #ccc; }
    h2 { color: #333; }
  </style>
</head>
<body>
  <h1>Multi-Agent Inventory Visuals</h1>
  <div id=\"charts\">
"""
    for img in images:
        html += f'    <h2>{img}</h2>\n'
        html += f'    <img src="visualizations/{img}" alt="{img}">\n'

    html += """
  </div>
  <div>
    <h2>Download Report</h2>
    <a href="simulation_report.csv" download>Download CSV Report</a>
  </div>
</body>
</html>
"""

    with open(output_html_path, "w") as f:
        f.write(html)

if __name__ == "__main__":
    main()
