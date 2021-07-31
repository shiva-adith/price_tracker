from stock_tracker import StockPrice
from news_tracker import NewsContent
from notification_manager import NotificationsManager

stock_to_track = input("Enter company name: ")

stock = StockPrice(stock_to_track)

# TODO Try using the Query Endpoint from Aplhavantage API.

print(stock.get_last_closing())
compare_prices = stock.compare_closing()
if type(compare_prices) is not bool:
    difference, direction_symbol, company_name, stock = compare_prices
    print(difference, direction_symbol, company_name, stock)
    stock_news = NewsContent(company_name=company_name, stock=stock)

    (headlines, briefs) = stock_news.get_company_news()

    notification = NotificationsManager(headlines=headlines,
                                        briefs=briefs,
                                        stock=stock,
                                        difference=difference,
                                        direction_symbol=direction_symbol)
    notification.send_stock_notifications()

else:
    print("Not a big difference")
