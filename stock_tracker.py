import os
import re
import sys
import requests
import pandas as pd
from pprint import pprint
from collections import namedtuple
from dotenv import dotenv_values

CONFIG = dotenv_values(".env")


class StockPrice:
    def __init__(self, company_name):
        # Stock API Info
        self.stock_url = "https://www.alphavantage.co/query?"
        self.company_name = company_name
        self.stock = self.get_stock_ticker()
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

    def get_stock_ticker(self):
        official_name = None
        ticker = None
        url = f'https://finnhub.io/api/v1/search?'
        params = {'q': self.company_name, "token": CONFIG.get("FINNHUB_API_KEY")}
        response = requests.get(url=url, params=params)
        # print(response)
        print(self.company_name)
        response.raise_for_status()
        data = response.json()
        pprint(data)
        if data.get("result"):
        # try:
            for item in data.get("result"):
                # API response might give multiple company profiles with similar names.
                # Regex matching is used to obtain the perfect match with the user's input.
                # Loops till a match is found.
                temp_name = re.search(f"{self.company_name}", item.get("description").lower())
                if temp_name:
                    official_name = item.get("description")
                    # ticker = item.get("displaySymbol")
                    temp_ticker = re.search(r"/", item.get("displaySymbol"))
                    if temp_ticker:
                        # Some symbols contain slashes, e.g GOOGL/USD.
                        # If found, the string is split and the content before the slash is retured.
                        ticker = item.get("displaySymbol").split("/")[0]
                    # ticker = item.get("symbol")
                    else:
                        ticker = item.get("displaySymbol")
                    # If match is found, break loop.
                    break

            print(f"Ticker: {ticker}\tName: {official_name}")
            self.company_name = official_name
            return ticker

            # official_name = data.get("result")[0].get("description")
            # ticker = data.get("result")[0].get("symbol")
            # print(ticker, official_name)

        # except (IndexError, TypeError):
        #     print("Please check the spelling in the company name and re-enter!")
        #     return False
        else:
            print("Unable to find the desired stock. Please check the spelling in the company name and re-enter.")
            return False
        # else:
        #     print("Please check your input again! I couldn't find any matches :/ ")

    def stock_api_response(self):
        response = requests.get(url=self.stock_url, params=self.stock_params)
        response.raise_for_status()
        print(response.status_code)
        all_stock_data = response.content
        print(all_stock_data)
        print(type(all_stock_data))

        # Sometimes, the API returns a success code (i.e 200) but the content is an Error message in bytes form.
        # Regex matching is done to see if the response contains Error Message in it.
        x = re.search("Error Message", all_stock_data.decode("utf-8"))

        if not x:
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
            # finally:
            with file:
                file.write(all_stock_data)

            file.close()
            self.get_stock_data()
        else:
            print("There was some error getting back stock-price info for this stock")
            sys.exit(1)

    def get_stock_data(self):
        try:
            csv_stock_data = pd.read_csv(f"{self.path}/TIME_SERIES_DAILY_ADJUSTED.csv", index_col=0)
        except FileNotFoundError:
            print("filenotfound error")
            csv_stock_data = pd.read_csv("TIME_SERIES_DAILY_ADJUSTED.csv", index_col=0)
        except Exception as err:
            print(f"Unexpected error opening data file is {repr(err)}")
            sys.exit(1)
        # finally:
        self.stock_data = csv_stock_data
        print(self.stock_data.head())
        # return self.stock_data

    def get_last_closing(self) -> float:
        yesterday_data = self.stock_data.iloc[0]
        yesterday_closing = yesterday_data.close
        yesterday_adjusted_closing = yesterday_data.adjusted_close
        if yesterday_closing != yesterday_adjusted_closing:
            print("They are not equal")
            return yesterday_adjusted_closing
        else:
            print("They are both equal")
            return yesterday_closing

    def compare_closing(self):
        day_before_data = self.stock_data.iloc[1]
        print(day_before_data)
        day_before_closing = day_before_data.close
        yesterday_closing = self.get_last_closing()
        print(f"Day before price: {day_before_closing}\nYesterday price: {yesterday_closing}")
        difference = (abs(yesterday_closing - day_before_closing)/day_before_closing) * 100

        if difference >= 0:
            results = namedtuple("Compare_Prices", ["difference", "direction_symbol", "company_name", "stock"])
            if yesterday_closing > day_before_closing:
                direction_symbol = "🔺"
            else:
                direction_symbol = "🔻"

            # stock_results = {"difference": difference,
            #                  "direction_symbol": direction_symbol,
            #                  "company_name": self.company_name,
            #                  "stock": self.stock}

            company_name = self.company_name
            stock = self.stock
            return results(difference, direction_symbol, company_name, stock)
            # return stock_results
        else:
            return False
# stock = StockPrice("tesla")
