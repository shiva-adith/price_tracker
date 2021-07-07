import requests
from dotenv import dotenv_values

CONFIG = dotenv_values(".env")


class NewsContent:
    def __init__(self, **kwargs):
        self.company_name = kwargs.get("company_name")
        self.stock = kwargs.get("stock")
        # self.headlines = None
        # self.briefs = None
        self.news_url = "https://newsapi.org/v2/everything?"
        self.news_params = {"apiKey": CONFIG.get("NEWS_API_KEY"), "qInTitle": f"{self.company_name}"}

    def get_company_news(self):
        headlines = []
        briefs = []
        response = requests.get(url=self.news_url, params=self.news_params)
        response.raise_for_status()
        print(f"News status code: {response.status_code}")

        top_articles = response.json().get("articles")[:3]
        print(top_articles)

        for article in top_articles:
            headlines.append(article.get('title'))
            briefs.append(article.get("description"))

        print(headlines)
        print(briefs)
        return headlines, briefs
