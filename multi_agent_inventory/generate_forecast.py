import pandas as pd

# Load your original demand data
df = pd.read_csv("demand_forecasting.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Sort data if needed
df = df.sort_values(by=['Product ID', 'Date'])

# Group by product and calculate a rolling average on sales quantity as forecast
df['forecasted_demand'] = df.groupby('Product ID')['Sales Quantity'].transform(lambda x: x.rolling(window=3, min_periods=1).mean().shift(-1))

# Save updated CSV
df.to_csv("demand_forecasting.csv", index=False)

print("Forecasted demand column added successfully!")