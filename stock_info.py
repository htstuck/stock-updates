import finnhub
import json
import smtplib
import email
import sys

def main():
    # Setup client
    with open('api_keys.json') as f1:
        FINNHUB_KEY = json.load(f1)['finnhub']
    finnhub_client = finnhub.Client(api_key=FINNHUB_KEY)

    # Load portfolio
    with open(sys.argv[1]) as f2:
        portfolio = f2.readlines()

    # portfolio_value = 0.0
    # todays_return = 0.0
    # movers = []

    for stock in portfolio:
        ticker, shares, price = tuple(stock.split(','))
        quote = finnhub_client.quote(ticker)
        get_stock_info(quote, ticker, int(shares), float(price))


# def get_porfolio_info(quote, ticker, shares, buy_price):
    # pass

def get_stock_info(quote, ticker, shares, buy_price):
    """Returns the daily information for a specific ticker."""
    # Get the quote for the given ticker
    close_yesterday = quote['pc']
    close_today = quote['c']
    open_today = quote['o']
    high_today = quote['h']
    low_today = quote['l']
    change = close_today - close_yesterday
    percent_change = change / close_yesterday * 100

    # Notify user with '*' if stock goes up/down by more than 5%
    if abs(percent_change) >= 5.0:
        ticker = "*  " + ticker 
    
    # Information as list of strings for easier formatting
    stock = ['\n', ticker, '~'*35]
    # Market value = close price * num of shares
    stock.append('Market Value ${:.2f}'.format(close_today * shares))
    # Number of shares
    stock.append('# of Shares: {}'.format(shares))
    # Today's return = (close price today - close price yesterday) * num of shares
    stock.append('Today\'s Return: {}  ({})'.format(as_currency(change * shares), as_percent(percent_change)))
    # Total return = (close today - buy price) * num of shares
    stock.append('Total Return: {}  ({})'.format(as_currency((close_today - buy_price) * shares), as_percent((close_today - buy_price) / buy_price * 100)))
    stock.append('-'*35)
    # Ticker open, close, high, and low for the day
    stock.append('Open: ${:.2f}   |   High: {:.2f}'.format(open_today, high_today))
    stock.append('Close: ${:.2f}  |   Low: {:.2f}'.format(close_today, low_today))

    # Print all data
    print('\n'.join(stock))


def as_currency(amount):
    if amount >= 0:
        return '+${:.2f}'.format(amount)
    else:
        return '-${:.2f}'.format(-amount)


def as_percent(percent):
    if percent >= 0:
        return '+{:.2f}%'.format(percent)
    else:
        return '-${:.2f}%'.format(percent)





if __name__ == "__main__":
    main()



