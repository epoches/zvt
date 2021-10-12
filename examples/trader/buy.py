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

    #大盘日线判断 日MACD 高于 昨日
    # kline = Stock1dHfqKdata.query_data(provider='joinquant', code='000300', return_type='df',
    #                                    start_timestamp=str(end_date), end_timestamp=str(start_date))



    for item in stocks_list:        # 遍历所有股票代码
        name = str(item).replace(".", "")  # 将股票的代码处理成我们需要的格式
        # 获取k线
        kline = Stock1dHfqKdata.query_data(provider='joinquant', code=item, return_type='df',
                                           start_timestamp=str(end_date), end_timestamp=str(start_date))
        #print(kline)
        if len(kline) < 60:             # 容错处理，因为有些新股可能k线数据太短无法计算指标
            continue
        ma5 = ta.MA(pd.Series(kline['close']), timeperiod=5, matype=0).tolist()        # 计算ma5和ma60
        ma60 = ta.MA(pd.Series(kline['close']), timeperiod=60, matype=0).tolist()
        # 剔除60日线向下的。
        if ma60[-1]<ma60[-2] and ma60[-2]<ma60[-3]:
            continue
        #RSI<20
        rsi = ta.RSI(pd.Series(kline['close']),timeperiod=6).tolist()
        #print(str(rsi[-1]))
        #BIAS3 < 10
        kline['bias_24'] = (pd.Series(kline['close']) - pd.Series(kline['close']).rolling(24, min_periods=1).mean()) / pd.Series(kline['close']).rolling(24,min_periods=1).mean() * 100
        #print(kline['bias_24'])
        #月macd
        delta = datetime.timedelta(days=1200)
        n_days = now - delta
        yue_date = n_days.strftime('%Y-%m-%d')
        dfmon = Stock1monHfqKdata.query_data(provider='joinquant', code=item, return_type='df',
                                             columns=['id','code','name','timestamp','close'],index='timestamp',
                                             start_timestamp=str(yue_date), end_timestamp=str(start_date))#.values
        #macd=get_macd_data(dfmon,12,26,9)
        print(dfmon)
        # 将价格数据转化成float类型
        dfmon['index'] = dfmon['timestamp'].rank(ascending=1, method='first')
        print(dfmon)
        close = [float(x) for x in dfmon['close']]
        macdDIFF, macdDEA, macd = ta.MACDEXT(dfmon, fastperiod=12, fastmatype=1, slowperiod=26, slowmatype=1,
                                             signalperiod=9, signalmatype=1)
        macd = macd * 2
        print(macd)
        #print(str(dtime[0])+'  dif  '+str(dif[0])+'  dea  '+str(dea[0])+'  macd  '+str(macd[0]))
        #print(macd)
        last = len(macd)
        #print(last)
        if last>1:
            macdmacd = macd['data_macd'][last-1]
            #print(macdmacd)
            #月MACD>0 且 月MACD增加 双均线交叉
            if macdmacd >0 and macdmacd > macd['data_macd'][last-2] and ma5[-1] > ma60[-1] and ma5[-2] <= ma60[-1]:
                stocks_pool.append(name)

    print(list(set(stocks_pool)))
    end_time = datetime.datetime.now()    # 获取本地时间
    print("筛选股票结束时间：", end_time)
