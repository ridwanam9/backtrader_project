import backtrader as bt
import pandas as pd

class SMAStrategy(bt.Strategy):
    def __init__(self):
        self.sma_fast = bt.indicators.SimpleMovingAverage(period=10)
        self.sma_slow = bt.indicators.SimpleMovingAverage(period=30)

    def next(self):
        if not self.position:
            if self.sma_fast[0] > self.sma_slow[0]:
                print("BUY")
                self.buy()
        else:
            if self.sma_fast[0] < self.sma_slow[0]:
                print("SELL")
                self.sell()

# engine
cerebro = bt.Cerebro()
cerebro.addstrategy(SMAStrategy)

# load data
df = pd.read_csv("data.csv", skiprows=3)

df.columns = ['date', 'close', 'high', 'low', 'open', 'volume']
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

for col in ['open', 'high', 'low', 'close', 'volume']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.dropna(inplace=True)

print(df.head())
print(df.dtypes)

# 🔥 WAJIB: masuk ke backtrader
data = bt.feeds.PandasData(dataname=df)
cerebro.adddata(data)

# modal
cerebro.broker.setcash(10000)

print("Modal awal:", cerebro.broker.getvalue())

# run
cerebro.run()

print("Modal akhir:", cerebro.broker.getvalue())

# chart
cerebro.plot(style='candlestick')