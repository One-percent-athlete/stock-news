import requests
from datetime import datetime as dt, timedelta
import smtplib
import os
import dotenv
dotenv.load_dotenv()

my_email = os.environ.get("my_email")
password = os.environ.get("password")
stock_api = os.environ.get("stock_api")
news_api = os.environ.get("news_api")

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

news_url="https://newsapi.org/v2/everything"
stock_url = 'https://www.alphavantage.co/query'

today = dt.now()
yesterday = today - timedelta(1)
db_yesterday = today - timedelta(2)
yesterday = yesterday.strftime("%Y-%m-%d")
db_yesterday = db_yesterday.strftime("%Y-%m-%d")


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

params={
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK,
    "apikey": stock_api
}

r = requests.get(stock_url,params=params)
data = r.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = yesterday_data["4. close"]

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))

percentage = (difference / float(yesterday_closing_price)) * 100

if percentage > 5:

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
    
    news_params={
        "q":"tesla",
        "from":today,
        "sortBy":"publishedAt",
        "apiKey": news_api
    }
    r = requests.get(news_url,params=news_params)
    data = r.json()["articles"]
    articles = data[:3]
        # data["articles"][0]["author"]
    for article in articles:
        title = article["title"]
        description = article["description"]
        msg = f"Subject:Tesla \n\n {title}: {description}" 
        # message = ["\n".join(msg.replace(u'\xe9', u' ')) for msg in description]
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email, 
                to_addrs=my_email, 
                msg=msg)

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

