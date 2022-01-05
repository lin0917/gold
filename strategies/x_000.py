from dateutil.relativedelta import relativedelta
from datetime import datetime

import backtrader as bt
class SIP(bt.Strategy):
    def __init__(self):
        self._next_buy_date = datetime(2010, 7, 1)#第一次購買日期
    
    def next(self):
        if self.data.datetime.date() >= self._next_buy_date.date():
            self._next_buy_date += relativedelta(weeks=2)
            
            print(f'=== {self.data.datetime.date()} 購買 1 股 價格 {self.data.close[0]} ===')
            
            self.buy(size=1)