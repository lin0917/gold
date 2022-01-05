import backtrader as bt

#策略跑出來的圖越接近在一個範圍內表示不會大起大落就是一個相對穩定的策略，相對風險低安全的一個策略
class BuyBuyBuy(bt.Strategy):
  def log(self, txt, dt=None):
    ''' 買買買 策略 '''
    dt = dt or self.datas[0].datetime.date(0)
    print(f'{dt.isoformat()}, {txt}')

  def __init__(self):
    # 鎖定"收盤價"在 datas[0] 的收盤價
    self.dataclose = self.datas[0].close
    self.order = None #訂單的變數確保在next()每一次調用的時候，可以知道有沒有訂單的狀況
  #當訂單被放置時就會call notify_order()就會收到訂單資訊
  def notify_order(self, order):
    if order.status in [order.Submitted, order.Accepted]:
      return 
    if order.status in [order.Completed]:
      if order.isbuy():
        self.log(f'已購買於 {order.executed.price}')
      elif order.issell():
        self.log(f'已賣出於 {order.executed.price}')

      self.bar_executed = len(self)#總共有多少個K線

    self.order = None #只要訂單被放置就會把order清空

  def next(self):
    self.log(f'收盤價, {self.dataclose[0]}')#最新的收盤價是多少
    
    # 假設沒有倉位(股票資產)就會去買
    if not self.position:
      # 今日收盤價 < 昨日收盤價
      if self.dataclose[0] < self.dataclose[-1]:
        
        # 昨日收盤價 < 前日收盤價 兩個條件都符合才是連三天跌
        if self.dataclose[-1] < self.dataclose[-2]:
          self.log(f'購買信號, {self.dataclose[0]}')
          self.order = self.buy()
    # 否則就會去賣，self.bar_executed + 5在5個K線生成後就賣
    else:
      if len(self) >= (self.bar_executed + 5):
        self.log(f'賣出信號 {self.dataclose[0]}')
        self.order = self.sell()#把賣出的細節全部綁定到order裡面
        