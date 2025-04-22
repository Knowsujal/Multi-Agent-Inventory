import logging

import warehouse_agent

class StoreAgent:
    def __init__(self, product_id, current_stock, lead_time_days, reorder_point):
        self.product_id = product_id
        self.current_stock = current_stock
        self.lead_time_days = lead_time_days
        self.reorder_point = reorder_point
        self.logger = logging.getLogger(f"StoreAgent-{product_id}")

    def evaluate_and_order(self, forecasted_demand, warehouse_agent):
        self.logger.info(f"Evaluating stock for Product ID {self.product_id}")
        reorder_needed = forecasted_demand > self.current_stock

        if reorder_needed:
            reorder_quantity = max(0, forecasted_demand - self.current_stock + self.reorder_point)
            self.logger.info(f"Requesting reorder of {reorder_quantity} units from warehouse")
            fulfilled_quantity = warehouse_agent.fulfill_order(self.product_id, reorder_quantity)

            if fulfilled_quantity > 0:
                self.current_stock += fulfilled_quantity
                self.logger.info(f"Received {fulfilled_quantity} units from warehouse.")
            else:
                self.logger.warning(f"Warehouse out of stock for Product ID {self.product_id}. Requested: {reorder_quantity}")
        else:
            self.logger.info("Stock sufficient. No reorder needed.")