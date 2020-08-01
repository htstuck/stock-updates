import finnhub
import smtplib
import email
import sys
import os 

def main():
    # Setup client
    PRIVATE_API_KEY = os.environ.get('PRIVATE_API_KEY')
    finnhub_client = finnhub.Client(api_key=PRIVATE_API_KEY)

    # Load portfolio
    with open(sys.argv[1]) as f2:
        portfolio = f2.readlines()

    total_portfolio_val, total_return_today, total_close_yesterday = 0.0, 0.0, 0.0
    big_movers = []
    stocks = []
    for stock in portfolio:
        # Get components of stock information
        ticker, shares, price = tuple(stock.split(','))
        shares = int(shares)
        buy_price = float(price)
        # Get the quote for the given ticker
        quote = finnhub_client.quote(ticker)
        # Important stats
        close_yesterday = quote['pc']
        close_today = quote['c']
        open_today = quote['o']
        high_today = quote['h']
        low_today = quote['l']
        change = close_today - close_yesterday
        percent_change = change / close_yesterday * 100

        # Collect overall portolfio data
        total_portfolio_val += close_today * shares
        total_return_today +=  change * shares
        total_close_yesterday += close_yesterday

        # Notify user with '*' if stock goes up/down by more than 5%
        if abs(percent_change) >= 5.0:
            ticker = "*  " + ticker 
            big_movers.append(ticker)
        
        # Information as list of strings for easier formatting
        stock = ['\n', ticker, '~'*35]
        # Today's return = (close price today - close price yesterday) * num of shares
        stock.append('Today\'s Return: {}  ({})'.format(as_currency(change * shares), as_percent(percent_change)))
        # Total return = (close today - buy price) * num of shares
        stock.append('Total Return: {}  ({})'.format(as_currency((close_today - buy_price) * shares), as_percent((close_today - buy_price) / buy_price * 100)))
        stock.append('-'*35)
        # Market value = close price * num of shares
        stock.append('Market Value ${:.2f}'.format(close_today * shares))
        # Number of shares
        stock.append('# of Shares: {}'.format(shares))

        stock.append('-'*35)
        # Ticker open, close, high, and low for the day
        stock.append('Open: ${:.2f}   |   High: {:.2f}'.format(open_today, high_today))
        stock.append('Close: ${:.2f}  |   Low: {:.2f}'.format(close_today, low_today))

        stocks.append(stock)
    # Print overall data
    print('~'*35)
    print('YOUR PORTFOLIO')
    print('~'*35)
    print('Total Portolfio Value: ${:.2f}'.format(total_portfolio_val))
    print('Today\'s Return: {} ({})'.format(as_currency(total_return_today), as_percent(total_return_today / total_close_yesterday * 100)))
    print('Big Movers:', ', '.join(big_movers))
    # Print indv. stock data
    for stock in stocks:
        print('\n'.join(stocks))


def as_currency(amount):
    if amount >= 0:
        return '+${:.2f}'.format(amount)
    else:
        return '-${:.2f}'.format(-amount)


def as_percent(percent):
    if percent >= 0:
        return '+{:.2f}%'.format(percent)
    else:
        return '-{:.2f}%'.format(abs(percent))


if __name__ == "__main__":
    main()



