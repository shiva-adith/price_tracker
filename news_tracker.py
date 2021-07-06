import requests
from twilio.rest import Client
from dotenv import dotenv_values

CONFIG = dotenv_values(".env")


class NewsContent:
    def __init__(self, **kwargs):
        self.difference = round(kwargs.get("difference"), 3)
        self.direction_symbol = kwargs.get("direction_symbol")
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

    def send_news_notifications(self):
        headlines, briefs = self.get_company_news()

        print("NEWS HEADLINES----------------")
        for headline, brief in zip(headlines, briefs):
            client = Client(CONFIG.get("TWILIO_ACCOUNT_SID"), CONFIG.get("TWILIO_AUTH_TOKEN"))

            body = f"{self.stock} {self.direction_symbol}: {self.difference}%\n\nHeadlines:\t{headline}:\n\n{brief}"

            message = client.messages.create(body=body,
                                             from_=CONFIG.get("FROM_WHATSAPP_NUMBER"),
                                             to=CONFIG.get("TO_NUMBER"))
            print(message.status)
            print(message.error_message)
            print(f"{self.stock} {self.direction_symbol}: {self.difference}%\n"
                  f"Headlines:\t{headline}:\n{brief}")
