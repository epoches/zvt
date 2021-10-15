#均线选股
from zvt.domain import Stock,Stock1dHfqKdata,Stock1monHfqKdata
from zvt.factors.algorithm import MaTransformer, MacdTransformer
from zvt.factors.technical_factor import TechnicalFactor
from zvt.contract import IntervalLevel
import numpy as np
import pandas as pd
import talib as ta
import datetime
import time

if __name__ == '__main__':
    stocks_pool = []                    # 空的股票池，将筛选出来的股票加入这个股票池中
    #获取当天和30天前的日期
    now = datetime.datetime.now()
    delta1 = datetime.timedelta(days=-1)

    delta = datetime.timedelta(days=120)
    n_days = now - delta
    start_date = now.strftime('%Y-%m-%d')
    print(start_date)
    end_date = n_days.strftime('%Y-%m-%d')
    print(end_date)
    #stocks_list = Stock.query_data(provider='joinquant')
    f = open(r"stocklist", 'r')
    s = f.read()
    f.close()
    stocks_list = s.split(',')
    #stocks_list = ['601928','002382','002978']
    #  获取沪深市场所有股票的基础信息

    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())    # 获取本地时间
    print("筛选股票开始时间：", start_time)

    #大盘日线判断 日MACD 高于 昨日

    for item in stocks_list:        # 遍历所有股票代码
        name = str(item).replace(".", "")  # 将股票的代码处理成我们需要的格式
        # 获取k线
        Stock1dHfqKdata.record_data(provider='joinquant', code=item)
        kline = Stock1dHfqKdata.query_data(provider='joinquant', code=item, return_type='df',
                                          start_timestamp=str(end_date), end_timestamp=str(now))
        #print(kline)
        if len(kline) < 60:             # 容错处理，因为有些新股可能k线数据太短无法计算指标
            continue
        rsi1 = ta.RSI(pd.Series(kline['close']), timeperiod=6).tolist()
        rsi2 = ta.RSI(pd.Series(kline['close']), timeperiod=12).tolist()
        rsi3 = ta.RSI(pd.Series(kline['close']), timeperiod=24).tolist()
        print('股票代码'+name+'.rsi1[-1]'+str(rsi1[-1])+'.rsi1[-2]'+str(rsi1[-2])+'.rsi2[-1]'+str(rsi2[-1])+'.rsi2[-2]'+str(rsi2[-2])+'.rsi1[-1]'+str(rsi3[-1])+'.rsi3[-2]'+str(rsi3[-2]))
        if rsi1[-1]<rsi1[-2] and rsi2[-1]<rsi2[-2] and rsi3[-1]<rsi3[-2]:
            stocks_pool.append(name)
    print('待卖出股票')
    print(list(set(stocks_pool)))
    end_time = datetime.datetime.now()    # 获取本地时间
    print("筛选股票结束时间：", end_time)
