import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "A3WHM9QRY5UCGQSU"
NEWS_API_KEY = "d072cb2b2ab341bcb75cefa1b58e2e28"
TWILIO_SID = "AC94009b0f16a12cbac58a72cd10ac1287"
TWILIO_AUTH_TOKEN = "40ac61050afdf0698cec8f51aef9b754"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

news_params = {
    "apiKey": NEWS_API_KEY,
    "q": COMPANY_NAME
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in stock_data.items()]

# Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries.
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "📈"
else:
    up_down = "📉"

# Find the difference between yesterday and day before yesterday stock prices
diff_percent = round(difference / float(yesterday_closing_price)) * 100

# If percentage difference is greater than 5 then fetch the relevant news articles
if abs(diff_percent) > 5:

    # Use the News API to get articles related to the COMPANY_NAME
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    # Use Python slice operator to create a list that contains the first 3 articles
    first_three_articles = articles[:3]

    # Create a new list of the first 3 article's headline and description using list comprehension
    formatted_articles = [f"{STOCK_NAME:{up_down}{diff_percent}}%\nHeadline: {article['title']}.\nBrief: {article['description']}" for article in first_three_articles]

    # Send each article as a separate message via Twilio
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_='+12342991016',
            to='+15198317960'
        )
