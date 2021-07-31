from twilio.rest import Client
from dotenv import dotenv_values

CONFIG = dotenv_values(".env")


class NotificationsManager:
    def __init__(self, **kwargs):
        self.headlines = kwargs.get("headlines")
        self.briefs = kwargs.get("briefs")
        self.stock = kwargs.get("stock")
        self.difference = round(kwargs.get("difference"), 3)
        self.direction_symbol = kwargs.get("direction_symbol")
        # self.to_num = CONFIG.get("TO_NUMBER")
        # self.from_num = CONFIG.get("FROM_WHATSAPP_NUMBER")

    def send_stock_notifications(self):
        print("NEWS HEADLINES----------------")
        for headline, brief in zip(self.headlines, self.briefs):
            client = Client(CONFIG.get("TWILIO_ACCOUNT_SID"), CONFIG.get("TWILIO_AUTH_TOKEN"))

            body = f"{self.stock} {self.direction_symbol}: {self.difference}%\n\nHeadlines:\t{headline}:\n\n{brief}"

            message = client.messages.create(body=body,
                                             from_=CONFIG.get("FROM_WHATSAPP_NUMBER"),
                                             to=CONFIG.get("TO_NUMBER"))
            print(message.status)
            print(message.error_message)
            print(f"{self.stock} {self.direction_symbol}: {self.difference}%\n"
                  f"Headlines:\t{headline}:\n{brief}")
