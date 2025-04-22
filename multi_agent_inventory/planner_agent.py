import os
import sys
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.logger import setup_logger

logger = setup_logger("PlannerAgent")

class PlannerAgent:
    def __init__(self, forecast_file):
        self.forecast_file = forecast_file
        self.data = self.load_data()  # ✅ Ensure data is loaded during initialization

    def load_data(self):
        """Load and preprocess forecast data."""
        try:
            df = pd.read_csv(self.forecast_file)
            
            # Debugging: Print actual column names
            print("CSV Columns Found:", df.columns.tolist())  # Debugging step
            
            df.columns = df.columns.str.strip()  # Remove extra spaces if any
            
            # Ensure required columns exist
            required_columns = {"Product ID", "forecasted_demand"}
            if not required_columns.issubset(df.columns):
                logger.error(f"Required columns {required_columns} are missing in the CSV.")
                print(f"Error: Required columns {required_columns} are missing in the CSV.")
                return None
            
            # Convert 'forecasted_demand' to numeric, replace NaNs with 0
            df["forecasted_demand"] = pd.to_numeric(df["forecasted_demand"], errors="coerce").fillna(0)

            logger.info("Data loaded successfully.")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            print(f"Error loading data: {e}")  # Debugging output
            return None
    def forecast_product(self, product_id):
        logger = self.setup_logger(product_id)
        logger.info(f"Starting forecast for Product ID: {product_id}")

        product_df = self.df[self.df['Product_ID'] == product_id].copy()
        product_df.set_index('Date', inplace=True)
        product_df = product_df.resample('D').sum()
        product_df['Sales'].fillna(0, inplace=True)

        try:
            model = ExponentialSmoothing(
                product_df['Sales'], trend='add', seasonal=None, initialization_method="estimated"
            )
            model_fit = model.fit()
            forecast = model_fit.forecast(self.forecast_horizon)

            logger.info(f"Forecast for next {self.forecast_horizon} days:\n{forecast}")
            print(f"📦 Product ID {product_id} forecast:\n{forecast}\n")
            return forecast

        except Exception as e:
            logger.error(f"Error forecasting Product ID {product_id}: {str(e)}")
            print(f"Error forecasting Product ID {product_id}: {str(e)}")
            return None

    def run_forecasting(self):
        if self.df is None:
            self.load_data()

        product_ids = self.df['Product_ID'].unique()
        print(f"Found {len(product_ids)} unique products.")

        for product_id in product_ids:
            self.forecast_product(product_id)

        print(" Forecasting completed for all products.")        

    def get_demand_forecast(self, product_id):
        """
        Return forecasted demand for a given product ID from preloaded data.
        """
        if self.data is not None:
            try:
                forecast_value = self.data.loc[self.data['Product ID'].astype(str) == str(product_id), 'forecasted_demand'].mean()
                return forecast_value if pd.notna(forecast_value) else 0
            except Exception as e:
                logger.error(f"Error retrieving forecast: {e}")
                return 0
        else:
            logger.warning("Data not loaded; returning forecast 0.")
            return 0