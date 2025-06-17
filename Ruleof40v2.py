"""
Rule of 40 Stock Screener
***Stanford Code In Place final project***
6/14/25
By: Jude Fauteux

The "Rule of 40" in finance, is a benchmark that suggests a healthy company's
combined annual revenue growth rate and profit margin should equal or exceed 40%.
This threshold was popularized as a benchmark to assess a company's financial health
and potential, balancing growth with profitability.

This program will calculate the "rule of 40" value for all S&P 500 stocks.
Only the stocks that are above or equal to 40% will be displayed.
If there is missing data from Yahoo and the calculation cannot be completed
then the stock ticker and missing data message is displayed.

The program was run and tested using the PyCharm IDE so that additional libraries
could be installed. It is not possible to install these libraries in the Code In Place IDE.
This program uses the financial data from Yahoo Finance (yfinance library)
"""

#Import libraries used in program
import yfinance as yf
import pandas as pd

#supress deprecation warnings from being displayed in console
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, message=".*Downcasting object dtype*")

#Compile list of stocks with missing financial data
ERROR_LIST = []

# fetch a current list of stock symbols for all 500 stocks in the S&P500 index
def fetch_sp500_tickers():
    """ Fetch S&P 500 tickers directly from Wikipedia """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    table = pd.read_html(url, header=0)
    tickers = table[0]['Symbol'].tolist()
    return tickers

#Calculate the Rule of 40 for the stock symbol passed as an argument,
#then print on the console if it is equal to of above 40%.
def calculate_rule_of_40(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)

    # Get annual income statement
    income_statement = ticker.financials
    #TRY statement is necessary to avoid crash when financial data
    #is unavailable from Yahoo Finance. Error is added to list.
    try:
        revenues = income_statement.loc["Total Revenue"].sort_index()
        operating_income = income_statement.loc["Operating Income"].sort_index()
    except KeyError as e:
        error = str(e)
        ERROR_LIST.append(ticker_symbol + " has missing data: " + error)
        return

    # Calculate most recent YoY revenue growth
    revenue_growth = revenues.pct_change() * 100
    latest_revenue_growth = revenue_growth.iloc[-1]

    # Calculate latest operating margin
    latest_operating_margin = (operating_income.iloc[-1] / revenues.iloc[-1]) * 100

    # Rule of 40 = Revenue Growth + Operating Margin
    rule_of_40 = latest_revenue_growth + latest_operating_margin

    # Output: If rule of 40 is met or surpassed, the ticker symbol and data
    # will be displayed.
    if rule_of_40 >= 40:
        #print(f"📊 {ticker_symbol} - Rule of 40 Calculation")
        print(f"✅ {ticker_symbol} - Rule of 40 Score: {rule_of_40:.1f}%")
        #print(f"✅ Rule of 40 Score: {rule_of_40:.2f}%")
        print(f"Latest YoY Revenue Growth: {latest_revenue_growth:.2f}% & ", end="")
        print(f"Latest Operating Margin: {latest_operating_margin:.2f}%")
        print()


#Main program
#fetches all current stock symbols in S&P500
#for each stock, calculate "Rule of 40" and print only if above 40%
#then finally print list of stocks missing financial data when rule of 40 can't be calculated.
def main():

    #Print purpose of program and S&P500 ticker symbols
    print("📊 This program will display stocks that surpass the 'rule of 40' benchmark for all S&P 500 stocks.")
    #fetch all current ticker symbols for S&P500 stock index
    tickers = fetch_sp500_tickers()
    print("S&P500 ticker symbols: ", tickers)

    #calculate rule of 40 for all ticker symbols fetched.
    for ticker in tickers:
        calculate_rule_of_40(ticker)

    #print list of stocks with missing financial data.
    if ERROR_LIST:
        print("\u2757\uFE0F Missing data: The 'Rule of 40' could not be calculated for the following stocks.")
        for item in ERROR_LIST:
            print(item)

    print("\U0001F6D1Rule of 40 Screening complete.")

if __name__ == "__main__":
    main()