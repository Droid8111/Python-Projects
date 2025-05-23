This Python script checks the stock price changes of Nvidia (NVDA) and sends a news update if the price fluctuates by 5% or more between two consecutive days. Here's a breakdown of what each part of the code does:

Steps Overview:
Stock Price Change Calculation:

The script uses the Alpha Vantage API to fetch daily stock price data for Nvidia (NVDA).
It compares the closing prices of the stock for yesterday and the day before yesterday.
If the percentage change between the two days exceeds 5%, it will print "Get News", otherwise, it will print "Don't get news".
Fetching News Articles:

If the stock price fluctuates by 5% or more, the script then uses the News API to fetch recent news articles related to "Nvidia Corporation."
It prints out the top 3 headlines and a brief description of each article.
Displaying the Results:

The stock price change is displayed as either an upward or downward trend (using "🔺" or "🔻").
It prints the percentage change along with the top 3 news articles about Nvidia