import requests
from twilio.rest import Client
from datetime import date
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
data = response1.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
today_date = str(date.today())
y_date = data_list[0]
by_date = data_list[1]
y_price = float(y_date["4. close"])
by_price = float(by_date["4. close"])
price_diff = by_price - y_price
percentage_change = round(abs(by_price - y_price) / by_price * 100, 1)
if percentage_change > 5:
    send_news = True
if price_diff > 0:
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
articles = response2.json()["articles"]
three_articles = articles[:3]
if price_increase:
    symbol = "🔺"
else:
    symbol = "🔻"
formatted_articles = [
    f'{STOCK}: {symbol}{percentage_change}%\nHeadline: {item["title"]}\nDescription: {item["description"]}\n' for item
    in three_articles]

if send_news:
    client = Client(account_sid, auth_token)
    for send_message in formatted_articles:
        message = client.messages.create(body=send_message,
                                         from_="+16076009148",
                                         to="+447536128991"
                                         )
        print(message.status)
