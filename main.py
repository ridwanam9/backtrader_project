import backtrader as bt
import pandas as pd

class SNRStrategy(bt.Strategy):
    params = dict(
        lookback=20,   # untuk cari support/resistance
        tolerance=0.01 # toleransi dekat SNR (1%)
    )

    def __init__(self):
        self.dataclose = self.data.close
        self.dataopen = self.data.open

    # 🔍 detect bullish engulfing
    def bullish_engulfing(self):
        return (
            self.dataclose[0] > self.dataopen[0] and
            self.dataclose[-1] < self.dataopen[-1] and
            self.dataclose[0] > self.dataopen[-1] and
            self.dataopen[0] < self.dataclose[-1]
        )

    # 🔍 detect bearish engulfing
    def bearish_engulfing(self):
        return (
            self.dataclose[0] < self.dataopen[0] and
            self.dataclose[-1] > self.dataopen[-1] and
            self.dataclose[0] < self.dataopen[-1] and
            self.dataopen[0] > self.dataclose[-1]
        )

    def next(self):
        if len(self.data) < self.params.lookback:
            return

        # 📊 ambil support & resistance
        recent_lows = self.data.low.get(size=self.params.lookback)
        recent_highs = self.data.high.get(size=self.params.lookback)

        support = min(recent_lows)
        resistance = max(recent_highs)

        price = self.dataclose[0]

        # 📏 cek apakah dekat SNR
        near_support = price <= support * (1 + self.params.tolerance)
        near_resistance = price >= resistance * (1 - self.params.tolerance)

        # 🔼 BUY
        if not self.position:
            if near_support and self.bullish_engulfing():
                size = self.broker.getcash() * 0.1 / price
                self.buy(size=size)
                self.stop_loss = price * 0.98
                self.take_profit = price * 1.04

        # 🔽 SELL
        else:
            if near_resistance and self.bearish_engulfing():
                print("SELL at", price)
                self.sell()

# engine
cerebro = bt.Cerebro()
cerebro.addstrategy(SNRStrategy)

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