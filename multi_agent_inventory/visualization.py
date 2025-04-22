import matplotlib.pyplot as plt

def plot_stock_levels(stock_history):
    plt.plot(stock_history)
    plt.title(" Stock Levels Over Time")
    plt.xlabel("Day")
    plt.ylabel("Stock")
    plt.show()

def plot_forecast_vs_actual(forecast, actual):
    plt.plot(forecast, label="Forecast")
    plt.plot(actual, label="Actual")
    plt.legend()
    plt.title(" Forecast vs Actual Demand")
    plt.show()