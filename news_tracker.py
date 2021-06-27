import os
import sys
import requests
from dotenv import dotenv_values

CONFIG = dotenv_values(".env")


class NewsContent:
    def __init__(self):
        self.news_url = "https://newsapi.org/v2/everything?"
        self.news_params = {"apiKey": CONFIG.get("NEWS_API_KEY"), "qInTitle": COMPANY_NAME}
