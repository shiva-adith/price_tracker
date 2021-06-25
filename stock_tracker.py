import os
import sys
import requests
import pandas as pd
from dotenv import dotenv_values

CONFIG = dotenv_values(".env")


class StockPrice:
    def __init__(self):
        # Stock API Info
        self.stock_url = "https://www.alphavantage.co/query?"
        self.stock = "TSLA"
        self.company_name = "Tesla"
        self.stock_data = None
        self.api_key = CONFIG.get('STOCK_API_KEY')
        self.direction_symbol = None
        self.stock_params = {"function": "TIME_SERIES_DAILY_ADJUSTED",
                             "symbol": self.stock,
                             "apikey": self.api_key,
                             "datatype": "csv"}
        self.current_dir = os.getcwd()
        self.data_dir = "data"
        self.path = os.path.join(self.current_dir, self.data_dir)
        self.stock_api_response()

    def stock_api_response(self):
        response = requests.get(url=self.stock_url, params=self.stock_params)
        response.raise_for_status()
        all_stock_data = response.content

        try:
            os.makedirs(self.path)
            print("Data Directory has been created successfully")
        except (OSError, FileExistsError):
            print("Directory already exists or cant be created! Please check path")

        try:
            file = open(f"{self.path}/TIME_SERIES_DAILY_ADJUSTED.csv", mode="wb")
        except FileNotFoundError:
            file = open("TIME_SERIES_DAILY_ADJUSTED.csv", mode="wb",)
        except Exception as err:
            print(f"Unexpected error opening data file is {repr(err)}")
            sys.exit(1)
        finally:
            with file:
                file.write(all_stock_data)

            file.close()
            self.get_stock_data()

    def get_stock_data(self):
        try:
            csv_stock_data = pd.read_csv(f"{self.path}/TIME_SERIES_DAILY_ADJUSTED.csv", index_col=0)
        except FileNotFoundError:
            csv_stock_data = pd.read_csv("TIME_SERIES_DAILY_ADJUSTED.csv", index_col=0)
        except Exception as err:
            print(f"Unexpected error opening data file is {repr(err)}")
            sys.exit(1)
        finally:
            self.stock_data = csv_stock_data
            print(self.stock_data.head())
            return self.stock_data

    def get_last_closing(self):
        yesterday_data = self.stock_data.iloc[0]
        last_closing = yesterday_data.close
        last_adjusted_closing = yesterday_data.adjusted_close
        if last_closing != last_adjusted_closing:
            print("They are not equal")
            return last_adjusted_closing
        else:
            print("They are both equal")
            return last_closing


# stock = StockPrice()
