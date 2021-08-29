from stock_tracker import StockPrice
from news_tracker import NewsContent
from notification_manager import NotificationsManager
from dotenv import dotenv_values
from flask import Flask, render_template, redirect, url_for

CONFIG = dotenv_values(".env")
app = Flask(__name__)
app.config['SECRET_KEY'] = CONFIG.get("FLASK_SECRET_KEY")


@app.route("/")
def home():
    return render_template("index.html")


def stock_app():
    stock_to_track = input("Enter company name: ")
    
    stock = StockPrice(stock_to_track)
    
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
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
