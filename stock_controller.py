import yfinance as yf
import pandas as pd
import datetime
import time
import datetime


def get_prices(ticker: str, start_time: int, end_time: int):
    start_date = datetime.datetime.fromtimestamp(start_time)
    end_date = datetime.datetime.fromtimestamp(end_time)
    data = yf.download(tickers=ticker,
                start=start_date,
                end=end_date,
                interval="1m")
    data.reset_index(inplace=True, drop=False)

    timestamps = []
    for date in data["Datetime"]:
        date_str = str(date).split("+")
        dt = datetime.datetime.strptime(date_str[0], "%Y-%m-%d %H:%M:%S")
        timestamps.append(int(dt.timestamp()))
    df = pd.DataFrame()
    df["Timestamps"] = timestamps
    df["Close"] = data["Close"]
    return df

""" start_date = datetime.datetime.fromtimestamp(time.time() - 5*24*60*60)
end_date = datetime.datetime.fromtimestamp(time.time())
data = yf.download(tickers="AAPL",
            start=start_date,
            end=end_date,
            interval="1m")
data.reset_index(inplace=True, drop=False)
print(data["Datetime"]) """