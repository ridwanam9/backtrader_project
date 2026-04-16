import backtrader as bt
import pandas as pd
import yfinance as yf


class SMAStrategy(bt.Strategy):
    def __init__(self):
        self.sma_fast = bt.indicators.SimpleMovingAverage(period=10)
        self.sma_slow = bt.indicators.SimpleMovingAverage(period=30)

    def next(self):
        if not self.position:
            if self.sma_fast > self.sma_slow:
                self.buy()
        else:
            if self.sma_fast < self.sma_slow:
                self.sell()

# engine
cerebro = bt.Cerebro()
cerebro.addstrategy(SMAStrategy)

# 🔥 load pakai pandas
df = pd.read_csv("data.csv", skiprows=3)

# rename kolom biar sesuai
df.columns = ['date', 'close', 'high', 'low', 'open', 'volume']

# ubah ke datetime
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# pastikan numeric
for col in ['open', 'high', 'low', 'close', 'volume']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.dropna(inplace=True)

print(df.head())
print(df.dtypes)