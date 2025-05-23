STOCK = "NVDA"
COMPANY_NAME = "Nvidia Corporation"
import requests #type: ignore


# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
api_key = "CTPUNF3YY9IBXJ0Q"
stock_endpoint = "https://www.alphavantage.co/query"
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": api_key
}
response = requests.get(stock_endpoint, params=stock_params)
# https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=CTPUNF3YY9IBXJ0Q  
response.raise_for_status()
data = response.json()
data_list = [value for (key, value) in data["Time Series (Daily)"].items()]
yesterday = data_list[0]
day_before_yesterday = data_list[1]
yesterday_close = float(yesterday["4. close"])
day_before_yesterday_close = float(day_before_yesterday["4. close"])
difference = abs(yesterday_close - day_before_yesterday_close)
percentage = (difference / yesterday_close) * 100

if percentage >= 5:
    print("Get News")
else:
    print("Don't get news")

# STEP 2: Use https://newsapi.org
news_api_key = "9acaf92dce714c43995df03b62156ea0"
news_endpoint = "https://newsapi.org/v2/everything"
news_params = {
    "q": COMPANY_NAME,
    "apiKey": news_api_key
}
news_response = requests.get(news_endpoint, params=news_params)
news_response.raise_for_status()
news_data = news_response.json()
articles = news_data["articles"]
three_articles = articles[:3]



## STEP 3: 

print("NVDA: ", end='')
if yesterday_close > day_before_yesterday_close:
    print("🔺", end='')
else:
    print("🔻", end='')
print(f"{percentage}%")

for article in three_articles:
    print("Headline:",article["title"])
    print("Brief:",article["description"])
    print("\n")

