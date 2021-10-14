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
import sys
from jqdatasdk import *
auth('19159862375', 'Yjbir=1977')

# macd指标
def get_macd_data(data, short=0, long1=0, mid=0):
    if short == 0:
        short = 12
    if long1 == 0:
        long1 = 26
    if mid == 0:
        mid = 9
    data['sema'] = pd.Series(data['close']).ewm(span=short).mean()
    data['lema'] = pd.Series(data['close']).ewm(span=long1).mean()
    data.fillna(0, inplace=True)
    data['data_dif'] = data['sema'] - data['lema']
    data['data_dea'] = pd.Series(data['data_dif']).ewm(span=mid).mean()
    data['data_macd'] = 2 * (data['data_dif'] - data['data_dea'])
    data.fillna(0, inplace=True)
    return data[['timestamp', 'data_dif', 'data_dea', 'data_macd']]


#当天收盘后执行
if __name__ == '__main__':
    stocks_pool = []                    # 空的股票池，将筛选出来的股票加入这个股票池中
    #获取当天和30天前的日期
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=240)
    n_days = now - delta
    start_date = now.strftime('%Y-%m-%d')
    print(start_date)
    end_date = n_days.strftime('%Y-%m-%d')
    print(end_date)
    #  获取选到的好股票的信息
    f = open(r"./data/goodcompany.txt", 'r')
    s = f.read()
    f.close()
    stocks_list = s.split(',')
    #stocks_list = Stock.query_data(provider='joinquant')
    #stocks_list = ['600019']


    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())    # 获取本地时间
    print("筛选股票开始时间：", start_time)


    szdf = get_price('000001.XSHG', start_date=str(end_date), end_date=str(start_date), frequency='1d')
    szclose = szdf['close'].values.tolist()
    print(szdf)
    if szclose[-1]<szclose[-2]:
        print('大盘不好，放弃买票')
        sys.exit()

    for item in stocks_list:        # 遍历所有股票代码
        name = str(item).replace(".", "")  # 将股票的代码处理成我们需要的格式
        # 获取k线
        kline = Stock1dHfqKdata.query_data(provider='joinquant', code=item, return_type='df',
                                           start_timestamp=str(end_date), end_timestamp=str(start_date))
        delta = datetime.timedelta(days=-2)
        n_days = now + delta
        p_date = n_days.strftime('%Y-%m-%d')
        Stock1dHfqKdata.record_data(provider='joinquant', code=item)
        klinep = Stock1dHfqKdata.query_data(provider='joinquant', code=item, return_type='df',
                                           start_timestamp=str(end_date), end_timestamp=p_date)
        if len(kline) < 60:             # 容错处理，因为有些新股可能k线数据太短无法计算指标
            continue
        #ma5 = ta.MA(pd.Series(kline['close']), timeperiod=5, matype=0).tolist()        # 计算ma5和ma60
        ma60 = ta.MA(pd.Series(kline['close']), timeperiod=60, matype=0).tolist()
        # 剔除60日线向下的。
        if ma60[-1]<ma60[-2] and ma60[-2]<ma60[-3]:
            continue
        rsi3 = ta.RSI(pd.Series(kline['close']),timeperiod=24).tolist()
        #rsip3 = ta.RSI(pd.Series(klinep['close']),timeperiod=24).tolist()

        close = kline['close'].values.tolist()
        if close[-1] > ma60[-1] and rsi3[-1]>50 and rsi3[-2]<50:
             stocks_pool.append(name)
    print('待购买股票：')
    print(list(set(stocks_pool)))
    end_time = datetime.datetime.now()    # 获取本地时间
    print("筛选股票结束时间：", end_time)
