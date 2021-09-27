from dotenv import dotenv_values
from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template, redirect, url_for
from stock_tracker import StockPrice
from news_tracker import NewsContent
from notification_manager import NotificationsManager
from data_handler import DataManager
from forms import RegistrationForm
from pprint import pprint
from werkzeug.security import generate_password_hash, check_password_hash

CONFIG = dotenv_values(".env")

app = Flask(__name__)
app.config['SECRET_KEY'] = CONFIG.get("FLASK_SECRET_KEY")
Bootstrap(app)


@app.route("/")
def home():
    stock_app()
    return render_template("index.html")


@app.route('/login')
def login():
    pass


@app.route("/logout")
def logout():
    pass


@app.route("/about")
def about():
    pass


@app.route("/contact")
def contact():
    pass


@app.route("/register")
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user_info = {"username": form.username.data,
                     "email": form.email.data,
                     "number": form.number.data,
                     "password": form.password.data}

        data = DataManager(user_info)
        if not data.check_user_exists(user=user_info):
            print("User Added")
            pprint(user_info)
        else:
            print("User is already registered!")


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
    app.run(debug=True)
