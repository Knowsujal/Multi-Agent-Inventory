def calculate_stockout_rate(sales, forecast):
    stockouts = sum([1 for s, f in zip(sales, forecast) if f > s])
    return stockouts / len(sales)

def calculate_turnover_rate(total_sales, avg_inventory):
    return total_sales / avg_inventory

def calculate_profit_margin(revenue, cost):
    return (revenue - cost) / revenue