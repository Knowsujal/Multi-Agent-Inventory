from store_agent import StoreAgent
from warehouse_agent import WarehouseAgent
from planner_agent import PlannerAgent  # Optional
from pricing_agent import PricingAgent  # Optional
import random
import matplotlib.pyplot as plt

# For tracking behavior over time
day_history = {}

def simulate_day(product_id, forecasted_demand, day):
    store = StoreAgent(
        product_id=product_id,
        current_stock=random.randint(30, 120),
        lead_time_days=5,
        reorder_point=100
    )
    warehouse = WarehouseAgent()
    warehouse.set_stock(product_id=product_id, quantity=500)

    print(f"\n🟢 Simulating day {day} for Product {product_id}")
    store.evaluate_and_order(forecasted_demand, warehouse)

    # Log behavior
    if product_id not in day_history:
        day_history[product_id] = []

    day_history[product_id].append({
        'day': day,
        'forecasted_demand': forecasted_demand,
        'store_stock': store.current_stock,
        'reorder_qty': max(0, forecasted_demand - store.current_stock),
    })

    print(f"📦 Warehouse final stock for Product {product_id}: {warehouse.get_stock(product_id)}")


def simulate_multiple_days(product_ids, days=7):
    for day in range(1, days + 1):
        print(f"\n========== Day {day} ==========")
        for product_id in product_ids:
            simulate_day(product_id, day)

    # After all simulations
    plot_inventory_behavior()


def plot_inventory_behavior():
    for product_id, data in day_history.items():
        days = [d['day'] for d in data]
        forecasted = [d['forecasted_demand'] for d in data]
        stock = [d['store_stock'] for d in data]
        reorder = [d['reorder_qty'] for d in data]

        plt.figure(figsize=(10, 6))
        plt.plot(days, forecasted, label='📈 Forecasted Demand', marker='o')
        plt.plot(days, stock, label='📦 Store Stock', marker='s')
        plt.plot(days, reorder, label='📬 Reorder Qty', marker='^')

        plt.title(f'Inventory Behavior for Product {product_id}')
        plt.xlabel('Day')
        plt.ylabel('Units')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
    
def plot_daily_summary(day, product_id, demand, stock, price):
        plt.figure(figsize=(10, 5))
        plt.bar(['Forecasted Demand', 'Stock', 'Price'], [demand, stock, price])
        plt.title(f'Day {day} Summary for Product {product_id}')
        plt.ylabel('Values')
        plt.savefig(f'outputs/day_{day}_product_{product_id}_summary.png')
        plt.close()


# Example usage
if __name__ == "__main__":
    simulate_multiple_days(product_ids=[1001, 1002], days=7)