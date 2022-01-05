import requests 
import json
import csv
import time
from dateutil.relativedelta import relativedelta
# import datetime 
from datetime import datetime
from backtrader import cerebro
from backtrader.analyzers.positions import PositionsValue
import pandas
import io
import os
import backtrader as bt
import matplotlib
# 互動圖表
from backtrader_plotting import Bokeh
# Tradimo 或 Blackly樣式
from backtrader_plotting.schemes import Blackly
import backtrader.analyzers as btanalyzers
#% matplotlib inline 
import matplotlib.pyplot as plt 
from strategies.buybuybuy import BuyBuyBuy
from strategies.x_000 import SIP
# from datetime import *
# import time


# 原文網址：https://kknews.cc/code/8p3b3jl.html

# input('請輸入一個代號')
# print(datetime.datetime)

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}
# input('輸入西元年月日')
s = requests.Session()

trick_No = input('請輸入一個代號')
# trick_No ='GOOG'
# 輸入起始日期跟結束日期
print('日期請用,隔開')
print('日期是個位數的請不要輸入空白')
# start_timestamp = int(datetime.datetime.timestamp(datetime.datetime(2015,9,6)))
# end_timestamp = int(datetime.datetime.timestamp(datetime.datetime(2020,9,4)))
star0 = input('輸入起始日期')
end0= input('輸入結束日期')
# star0='2016,10,18'
# end0='2019,10,18'
start_t = time.strptime(star0 , "%Y,%m,%d")
end_t = time.strptime(end0, "%Y,%m,%d")
print(star0)
print(end0)

import datetime 
start_timestamp = int(datetime.datetime.timestamp(datetime.datetime(start_t[0],start_t[1],start_t[2])))
end_timestamp = int(datetime.datetime.timestamp(datetime.datetime(end_t[0],end_t[1],end_t[2])))
print(start_timestamp)
print(end_timestamp)

url = f'https://query1.finance.yahoo.com/v7/finance/download/{trick_No}?period1={start_timestamp}&period2={end_timestamp}&interval=1d&events=history&includeAdjustedClose=true'

print(url)
# 發送get請求
r = s.get(url, headers=headers)
if r.status_code == requests.codes.ok:
    with open(f'data/{trick_No}.csv', 'w') as trick_csv:
        trick_csv.write(r.text)

API_KEY = '77IK4XCQEGARR8P3'

def getDataframeFromURL(url):
    dataString = requests.get(url).content
    result = pandas.read_csv(io.StringIO(dataString.decode('utf-8')), index_col=0)
    return result

def stockPriceIntraday(ticker, folder):
    # url = f'https://www.alphavantage.co/query?apikey={API_KEY}&function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=1min&outputsize=full&datatype=csv'
    intraday = getDataframeFromURL(url)

    print(intraday)
    fileName = f'{folder}/{ticker}.csv'

    if os.path.exists(fileName):
        history = pandas.read_csv(fileName, index=0)
        intraday.append(history)

    intraday.sort_index(inplace=True)

    intraday.to_csv(fileName)
    print(f'{ticker} 盤中資訊已儲存')
#自動刪除檔案
# import os
# import datetime

# scanned paths
Paths = './data/intraday'
# delete days
Dday = 1

def shouldkeep(file):
    if datetime.datetime.fromtimestamp( os.path.getmtime(file) ) > \
        datetime.datetime.now() - datetime.timedelta(Dday):
        return True


tickersRowData = pandas.read_csv(f'data/{trick_No}.csv')

# tickers = tickersRowData['Symbol'].tolist()

tickers = [trick_No] #每天只跑這幾支股票的下載

for i, ticker in enumerate(tickers):
    try:
        print(f'盤中價格 {i} / {len(tickers)}')
        stockPriceIntraday(tickers, folder='./data/intraday')
    except:
        pass
print('所有歷史股價已下載')

cerebro = bt.Cerebro()

cerebro.broker.setcash(1e5)

cerebro.broker.setcommission(
    commission=2.0,
    margin=2000.0,
    mult=10.0,
    name='Eurostoxxx50'
)

print(cerebro.addsizer(bt.sizers.SizerFix, stake=20))

from datetime import datetime
# Backtrader 提供了 Analyzers 這組工具來產生一些分析的數據，協助使用者來優化他們的策略
# 交易分析 (策略勝率)
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='TradeAnalyzer')

# 交易基本統計分析
cerebro.addanalyzer(bt.analyzers.PeriodStats, _name='PeriodStats')

# 回落統計 賠率到多少？風險控管的意思
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')

# 期望獲利/標準差 ＊每一年的交易次數開根號 System Quality Number
cerebro.addanalyzer(bt.analyzers.SQN, _name='SQN')

# 夏普指數 
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SharpeRatio')

#csv中的volumn是每一日的交易量，先去YahooFinance下載資料

# class SIP(bt.Strategy):
#     def __init__(self):
#         self._next_buy_date = datetime(2010, 7, 1)#第一次購買日期
    
#     def next(self):
#         if self.data.datetime.date() >= self._next_buy_date.date():
#             self._next_buy_date += relativedelta(weeks=2)
            
#             print(f'=== {self.data.datetime.date()} 購買 1 股 價格 {self.data.close[0]} ===')
            
#             self.buy(size=1)

class TestStrategy(bt.Strategy):
    def __init__(self):
        self._next_buy_date = datetime(2010,1,5)
    def next(self):
        if self.data.datetime.date() >= self._next_buy_date.date():
            self._next_buy_date += relativedelta(months=1)
            self.buy(slze=1)

cerebro = bt.Cerebro()#大腦

cerebro.broker.setcash(1e5)

cerebro.broker.setcommission(
    commission=0.001,
)
# start_t = time.strptime(start_t , "%Y, %m, %d")
# end_t = time.strptime(end_t, "%Y, %m, %d")
# print(time.struct_time(start_t))
# print(time.struct_time(end_t))

# if star0[5]==0:
#     star0[5]=' '
# if star0[8]==0:
#     star0[8]=' '
# if end0[5]==0:
#     end0[5]=' '
# if end0[8]==0:
#     end0[8]=' '
# print(star0)
# print(end0)
print('日期是個位數的請輸入空白注意起始月跟結束月不要輸入一樣')
# start_t = time.strptime(star0 , "%Y,%m,%d")
# end_t = time.strptime(end0, "%Y,%m,%d")
data = bt.feeds.YahooFinanceCSVData(
    # 股票資料位置 './data/TSLA.csv'
    dataname=f'./data/{trick_No}.csv',
    
    # 資料起始日
    fromdate=datetime(int(input('輸入起始年')),int(input('月')),int(input('日'))),
    # fromdate = datetime(start_t[0],start_t[1],start_t[2]),
    # 資料結束日
    # todate=datetime(end_t[0],end_t[1],end_t[2])

    todate =datetime(int(input('輸入結束年')),int(input('月')),int(input('日')))
    )
# print(data.fromdata)
# print(data.todata)
cerebro.adddata(data)
cerebro.addstrategy(BuyBuyBuy)
cerebro.addstrategy(TestStrategy)
cerebro.broker.set_cash=100000
# cerebro.plot()
cerebro.run()
plt.figure()
print('投資>結束資產 %.2f $' % cerebro.broker.getvalue())
cerebro.plot()

