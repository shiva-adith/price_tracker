from stock_tracker import StockPrice
from news_tracker import NewsContent

stock = StockPrice()
news = NewsContent()
print(stock.get_last_closing())
compare_prices = stock.compare_closing()
if type(compare_prices) is not bool:
    difference, direction_symbol, company_name = compare_prices

    print(difference, direction_symbol, company_name)
else:
    print("Not a big difference")
