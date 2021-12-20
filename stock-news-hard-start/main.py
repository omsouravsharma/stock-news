import requests
from twilio.rest import Client


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
API_KEY = "XXX"
API_KEY_STOCK = "XXX"


parameters_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY_STOCK
}


response_stock = requests.get(STOCK_ENDPOINT, params=parameters_stock)
response_stock.raise_for_status()
data_stock = response_stock.json()
print(data_stock)

yesterday = float(data_stock["Time Series (Daily)"]["2021-12-17"]["4. close"])
day_before_yesterday = float(data_stock["Time Series (Daily)"]["2021-12-16"]["4. close"])
print(yesterday)
print(day_before_yesterday)
difference = float(yesterday)-float(day_before_yesterday)
diff_percent = round((difference/yesterday)*100, 2)
up_down = None
if diff_percent > 0:
    up_down = "🚀"
else:
    up_down = "😥"
print(diff_percent)
print(difference)


if diff_percent > 0:

    parameters = {
        "q": STOCK,
        "from": '2021-12-19',
        "sortBy": "publishedAt",
        "apikey": API_KEY
    }

    response = requests.get(NEWS_ENDPOINT, params=parameters)
    response.raise_for_status()
    data = response.json()
    three_article = data['articles'][:3]
    print(three_article)


formatted_article = [f"{STOCK}: {up_down} {diff_percent}Headline: {article['title']}. \nBrief: {article['description']}" for article in three_article]

account_sid = 'XXXX'
auth_token = 'XXXX'
client = Client(account_sid, auth_token)

for article in formatted_article:
    message = client.messages \
                    .create(
                         body=article,
                         from_='+XXXXXXXXXXX',
                         to='+XXXXXXXXXXXXX'
                     )

print(message.sid)
