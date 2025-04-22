import logging
from collections import defaultdict

class WarehouseAgent:
    def __init__(self):
        # Holds stock of each product ID
        self.stock = {}

    def set_stock(self, product_id, quantity):
        self.stock[product_id] = quantity
        
    def get_stock(self, product_id):
        return self.stock.get(product_id, 0)

    def fulfill_order(self, product_id, quantity):
        available = self.stock.get(product_id, 0)  # ✅ Changed from self.inventory to self.stock

        if available >= quantity:
            self.stock[product_id] -= quantity
            print(f"[WarehouseAgent] Fulfilled order of {quantity} units for Product ID {product_id}")
            return quantity
        else:
            print(f"[WarehouseAgent] Insufficient stock for Product ID {product_id}. Available: {available}")
            return 0

    def prioritize_stores(self, demand_data):
        """Optional: Sort store requests by highest forecast demand (not implemented in comm. logic yet)."""
        return sorted(demand_data.items(), key=lambda x: x[1], reverse=True)
    
    def should_reorder(current_stock, reorder_point):
        return current_stock < reorder_point