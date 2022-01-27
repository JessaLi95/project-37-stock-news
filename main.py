import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from datetime import date, timedelta
from decouple import config

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
account_sid = "ACc107e0ac7ee9985e3cb27d60b694ff46"
auth_token = config('AUTH_TOKEN')

send_news = False
price_increase = True
url_stock = "https://www.alphavantage.co/query"
parameter1 = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": "958VF6WF58AF4PZW"
}
response1 = requests.get(url_stock, params=parameter1)
response1.raise_for_status()
data = response1.json()
today_date = str(date.today())
y_date = str(date.today() - timedelta(days=1))
by_date = str(date.today() - timedelta(days=2))
y_price = float(data["Time Series (Daily)"][y_date]["4. close"])
by_price = float(data["Time Series (Daily)"][by_date]["4. close"])
percentage_change = round((by_price - y_price) / y_price, 3)
if percentage_change < -0.05 or percentage_change > 0.05:
    send_news = True
if percentage_change < 0:
    price_increase = False

url_news = "https://newsapi.org/v2/everything"
parameter2 = {
    "q": COMPANY_NAME,
    "from": today_date,
    "sortBy": "popularity",
    "apiKey": "75cb2d89c6454b48869c95adbcbbdd13"
}
response2 = requests.get(url_news, params=parameter2)
response2.raise_for_status()
date2 = response2.json()
news_1 = f'Title: {date2["articles"][0]["title"]}\nDescription: {date2["articles"][0]["description"]}\n'
news_2 = f'Title: {date2["articles"][1]["title"]}\nDescription: {date2["articles"][1]["description"]}\n'
news_3 = f'Title: {date2["articles"][2]["title"]}\nDescription: {date2["articles"][2]["description"]}\n'
news = news_1 + news_2 + news_3
if price_increase:
    symbol = "TSLA: 🔺"
else:
    symbol = "TSLA: 🔻"
SMS_messages = f"{symbol}{percentage_change * 100}%\n{news}"

if send_news:
    # proxy_client = TwilioHttpClient()
    # proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(body=SMS_messages,
                from_="+16076009148",
                to="+447536128991"
                )
    print(message.status)
