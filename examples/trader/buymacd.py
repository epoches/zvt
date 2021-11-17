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
from jqdatasdk import *
auth('19159862375', 'Yjbir=1977')


#当天收盘后和第二天有区别
if __name__ == '__main__':
    stocks_pool = []                    # 空的股票池，将筛选出来的股票加入这个股票池中
    #获取当天和30天前的日期
    now = datetime.datetime.now()
    d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '9:30', '%Y-%m-%d%H:%M')
    if now<d_time:
        now = datetime.datetime.now() - datetime.timedelta(days=1)
    print(now)
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

    #大盘日线判断 日MACD 高于 昨日
    szdf = get_price('000001.XSHG', start_date=str(end_date), end_date=str(start_date), frequency='1d')
    szDIFF, szDEA, szmacd = ta.MACDEXT(szdf['close'], fastperiod=12, fastmatype=1, slowperiod=26, slowmatype=1,
                                 signalperiod=9, signalmatype=1)

    #szclose = szdf['close'].values.tolist()
    print(szmacd)
    if szmacd[-1]<szmacd[-2]:
        print('大盘不好，放弃买票')
        sys.exit()

    for item in stocks_list:        # 遍历所有股票代码
        name = str(item).replace(".", "")  # 将股票的代码处理成我们需要的格式
        # 获取k线
        Stock1dHfqKdata.record_data(provider='joinquant', code=item)
        kline = Stock1dHfqKdata.query_data(provider='joinquant', code=item, return_type='df',
                                           start_timestamp=str(end_date), end_timestamp=str(start_date))
        #print(kline[-1:])
        if len(kline) < 60:             # 容错处理，因为有些新股可能k线数据太短无法计算指标
            continue
        ma5 = ta.MA(pd.Series(kline['close']), timeperiod=5, matype=0).tolist()
        ma60 = ta.MA(pd.Series(kline['close']), timeperiod=60, matype=0).tolist()
        # 剔除60日线向下的。
        if ma60[-1]<ma60[-2] and ma60[-2]<ma60[-3]:
            continue
        rsi1 = ta.RSI(pd.Series(kline['close']), timeperiod=6).tolist()
        rsi3 = ta.RSI(pd.Series(kline['close']),timeperiod=24).tolist()
        kline['bias_24'] = (pd.Series(kline['close']) - pd.Series(kline['close']).rolling(24,min_periods=1).mean()) / pd.Series(
            kline['close']).rolling(24, min_periods=1).mean() * 100
        #print(kline['bias_24'])
        delta = datetime.timedelta(days=1200)
        n_days = now - delta
        yue_date = n_days.strftime('%Y-%m-%d')
        dfmon = Stock1monHfqKdata.query_data(provider='joinquant', code=item, return_type='df',
                                             columns=['id', 'code', 'name', 'timestamp', 'close'], index='timestamp',
                                             start_timestamp=str(yue_date), end_timestamp=str(start_date))  # .values

        dfmon['index'] = dfmon['timestamp'].rank(ascending=1, method='first')
        # close = [float(x) for x in dfmon['close']]
        DIFF, DEA, macd = ta.MACDEXT(kline['close'], fastperiod=12, fastmatype=1, slowperiod=26, slowmatype=1,
                                     signalperiod=9, signalmatype=1)
        mDIFF, mDEA, mmacd = ta.MACDEXT(dfmon['close'], fastperiod=12, fastmatype=1, slowperiod=26, slowmatype=1,
                                        signalperiod=9, signalmatype=1)
        macd = macd.values.tolist()
        mmacd = mmacd.values.tolist()

        close = kline['close'].values.tolist()
            #月MACD>0 且 月MACD增加 双均线交叉 and ma5[-2] <= ma60[-1]
        if macd[-2]<macd[-1] and mmacd[-1]>0 and mmacd[-2]<mmacd[-1] and  close[-1] > ma5[-1] and  close[-1] > ma60[-1] and rsi1[-1]<20 and kline['bias_24']<10 :
             stocks_pool.append(name)
    print('待购买股票：')
    print(list(set(stocks_pool)))
    end_time = datetime.datetime.now()    # 获取本地时间
    print("筛选股票结束时间：", end_time)
