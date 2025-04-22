# pricing_agent.py

import logging

class PricingAgent:
    def __init__(self, base_price, elasticity=-0.5):
        """
        Initialize PricingAgent.
        :param base_price: Base price of the product
        :param elasticity: Price elasticity of demand (default: -0.5)
        """
        self.base_price = base_price
        self.elasticity = elasticity
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger("PricingAgent")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def adjust_price(self, forecasted_demand, current_stock):
        """
        Adjust price based on forecasted demand and current stock.
        If demand is high and stock is low, increase price.
        If demand is low and stock is high, decrease price.
        """
        if current_stock == 0:
            self.logger.warning("Stock is zero. Price remains unchanged.")
            return self.base_price

        # Calculate demand-to-stock ratio
        ratio = forecasted_demand / current_stock

        # Simple elasticity-based pricing model
        price_multiplier = 1 + (self.elasticity * (1 - ratio))
        new_price = max(self.base_price * price_multiplier, 0.01)  # Ensure price never goes negative

        self.logger.info(f"Adjusted price from ${self.base_price:.2f} to ${new_price:.2f} (Forecasted demand: {forecasted_demand}, Stock: {current_stock})")

        return round(new_price, 2)