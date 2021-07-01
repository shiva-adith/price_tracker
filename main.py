from stock_tracker import StockPrice
from news_tracker import NewsContent

stock = StockPrice()

print(stock.get_last_closing())
compare_prices = stock.compare_closing()
if type(compare_prices) is not bool:
    difference, direction_symbol, company_name, stock = compare_prices
    print(difference, direction_symbol, company_name, stock)
    stock_news = NewsContent(difference, direction_symbol, company_name, stock)
    stock_news.send_news_notifications()
else:
    print("Not a big difference")
