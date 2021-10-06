import matplotlib.pyplot as plt
import talib as ta
import pandas as pd
from zvt.domain import Stock, Stock1dHfqKdata
# from matplotlib import rc
# rc('mathtext', default='regular')
import seaborn as sns
sns.set_style('white')
plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False # 用来正常显示负号
Stock1dHfqKdata.record_data(provider='joinquant', code='600563')
dw = Stock1dHfqKdata.query_data(provider='joinquant', entity_id='stock_sh_600563',
                                                         start_timestamp='2016-01-18',end_timestamp = '2016-07-18')
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1) #得到fig对象之后，通过add_subplot增加子图（返回了一个axes坐标轴），该方法需要三个参数，分别为：numrows, numcols, fignum。其中，一共有numrows*numcols个子图，即：将图表分为N行*M列，fignum标识了该子图的顺序，其范围从1到numrows*numcols。在上例中1,1,1表示了该绘图对象仅有1个子图，也就是1*1类型。
# ax2 = fig.add_subplot(1, 2, 2)
fig.suptitle('MACD测试', fontsize = 14, fontweight='bold')
ax1.set_title("股票收盘价")
ax1.set_xlabel("时间")
ax1.set_ylabel("价格")
# ax2.set_title("股票MACD")
# ax2.set_xlabel("时间")
# ax2.set_ylabel("MACD值")

#target_date = latest_day[0].timestamp
#close = dw['close']
# dw['macd'], dw['macdsignal'], dw['macdhist'] = ta.MACD(dw['close'], fastperiod=12, slowperiod=26, signalperiod=9)
# print(dw)
plt.subplots_adjust(bottom=0.13, top=0.95)
# sma5 = ta.SMA(dw['close'], timeperiod = 5)
# ax1.plot(dw['timestamp'],sma5)
# sma10 = ta.SMA(dw['close'], timeperiod = 10)
# ax1.plot(dw['timestamp'],sma10)
ax1.plot(dw['timestamp'],dw['close'])
# plt.legend(('daily', 'SMA5', 'SMA10'))
plt.grid(True)
#ax2.plot(dw['timestamp'],dw['macd'])
#dw[['close','macd','macdsignal','macdhist']].plot()
plt.show()