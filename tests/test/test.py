# -*- coding: utf-8 -*-
from zvt.contract import IntervalLevel
from zvt.factors.algorithm import MaTransformer, MacdTransformer
from zvt.factors.ma.ma_factor import CrossMaFactor
from ..context import init_test_context
from zvt.api import get_kdata
from zvt.contract import IntervalLevel
from zvt.contract.api import get_db_session
from jqdatasdk import *
import numpy as np
import pandas as pd
import talib
import datetime
import array
from zvt.domain import *
from zvt.domain import FinanceFactor, BalanceSheet, IncomeStatement, CashFlowStatement
from zvt.contract.api import get_db_session
from zvt.utils.time_utils import to_time_str

session = get_db_session(provider='eastmoney', db_name='finance')  # type: sqlalchemy.orm.Session

init_test_context()

from zvt.factors.technical_factor import TechnicalFactor

def test():
    auth('13956782345','Yjbir=1977')

    # 查询当日剩余可调用数据条数
    count = get_query_count()
    print(count)
    #获取MACD数据
    # factor = TechnicalFactor(provider='joinquant', codes=['000338'], start_timestamp='2021-05-01',
    #                          end_timestamp='2021-06-30', level=IntervalLevel.LEVEL_1DAY, computing_window=None,
    #                          transformer=MacdTransformer(), adjust_type='hfq')
    #print(factor.factor_df.tail())
    # compare with east money manually
    # diff = factor.factor_df['diff']
    # dea = factor.factor_df['dea']
    # macd = factor.factor_df['macd']
    #print(factor.factor_df)
    # print(str(macd))

    #获取 MA60日数据
    # factor = TechnicalFactor(provider='joinquant', codes=['000338'], start_timestamp='2019-01-01',
    #                          end_timestamp='2019-06-10', level=IntervalLevel.LEVEL_1DAY, computing_window=30,
    #                          transformer=MaTransformer(windows=[5, 10, 30, 60]), adjust_type='qfq')
    #
    # print(factor.factor_df.tail())
    #
    # # compare with east money manually
    # ma5 = factor.factor_df['ma5']
    # ma10 = factor.factor_df['ma10']
    # ma30 = factor.factor_df['ma30']
    # ma60 = factor.factor_df['ma60']
    # print(ma60)

    day_k_session = get_db_session(provider='joinquant',
                                   db_name='stock_1d_kdata')  # type: sqlalchemy.orm.Session
    df = get_kdata(entity_id='stock_sh_603220', session=day_k_session, level=IntervalLevel.LEVEL_1DAY,
                   provider='joinquant')
    print(df)
    #
    # rsi = talib.RSI(np.array(df['close']), 2)
    # print(str(rsi[-1]))

    # 查询当日剩余可调用数据条数
    # count = get_query_count()
    # print(count)

    # 计算方法：
    # bias指标
    # N期BIAS=(当日收盘价-N期平均收盘价)/N期平均收盘价*100%
    # df['bias_6'] = (df['close'] - df['close'].rolling(6, min_periods=1).mean()) / df['close'].rolling(6,
    #                                                                                                   min_periods=1).mean() * 100
    # df['bias_12'] = (df['close'] - df['close'].rolling(12, min_periods=1).mean()) / df['close'].rolling(12,
    #                                                                                                     min_periods=1).mean() * 100
    # df['bias_24'] = (df['close'] - df['close'].rolling(24, min_periods=1).mean()) / df['close'].rolling(24,
    #                                                                                                     min_periods=1).mean() * 100
    # df['bias_6'] = round(df['bias_6'], 2)
    # df['bias_12'] = round(df['bias_12'], 2)
    # df['bias_24'] = round(df['bias_24'], 2)
    #
    # print(df['bias_24'])

    # 威廉指标
    # 建议用talib库的WILLR方法，亲测有用
    # df['willr'] = ta.WILLR(df['high'], df['low'], df['close'], timeperiod=14)

    # macd指标
    # def get_macd_data(data, short=0, long1=0, mid=0):
    #     if short == 0:
    #         short = 12
    #     if long1 == 0:
    #         long1 = 26
    #     if mid == 0:
    #         mid = 9
    #     data['sema'] = pd.Series(data['close']).ewm(span=short).mean()
    #     data['lema'] = pd.Series(data['close']).ewm(span=long1).mean()
    #     data.fillna(0, inplace=True)
    #     data['data_dif'] = data['sema'] - data['lema']
    #     data['data_dea'] = pd.Series(data['data_dif']).ewm(span=mid).mean()
    #     data['data_macd'] = 2 * (data['data_dif'] - data['data_dea'])
    #     data.fillna(0, inplace=True)
    #     return data[['candle_begin_time_GMT8', 'data_dif', 'data_dea', 'data_macd']]

    # kdj指标
    # def myself_kdj(df):
    #     low_list = df['low'].rolling(9, min_periods=9).min()
    #     low_list.fillna(value=df['low'].expanding().min(), inplace=True)
    #     high_list = df['high'].rolling(9, min_periods=9).max()
    #     high_list.fillna(value=df['high'].expanding().max(), inplace=True)
    #     rsv = (df['close'] - low_list) / (high_list - low_list) * 100
    #     df['k'] = pd.DataFrame(rsv).ewm(com=2).mean()
    #     df['d'] = df['k'].ewm(com=2).mean()
    #     df['j'] = 3 * df['k'] - 2 * df['d']
    #     return df



    #企业净利润  见zvt\domain\fundamental\finance.py
    # correct_timestamps = ['2021-06-30', '2021-03-31','2019-20-30', '2020-06-30', '2020-03-31',
    #                       '2019-09-30', '2019-06-30', '2019-03-31','2018-09-30', '2018-06-30', '2018-03-31',
    #                       '2017-12-31', '2017-09-30', '2017-06-30',
    #                       '2017-03-31', '2016-12-31', '2016-09-30', '2016-06-30', '2016-03-31', '2015-12-31',
    #                       '2015-09-30', '2015-06-30', '2015-03-31', '2014-12-31', '2014-09-30', '2014-06-30',
    #                       '2014-03-31', '2013-12-31', '2013-09-30', '2013-06-30', '2013-03-31', '2012-12-31',
    #                       '2012-09-30', '2012-06-30', '2012-03-31', '2011-12-31', '2011-09-30', '2011-06-30',
    #                       '2011-03-31', '2010-12-31', '2010-09-30', '2010-06-30', '2010-03-31', '2009-12-31',
    #                       '2009-09-30', '2009-06-30', '2009-03-31', '2008-12-31', '2008-09-30', '2008-06-30',
    #                       '2008-03-31', '2007-12-31', '2007-09-30', '2007-06-30', '2007-03-31', '2006-12-31',
    #                       '2006-09-30', '2006-06-30', '2006-03-31', '2005-12-31', '2005-09-30', '2005-06-30',
    #                       '2005-03-31', '2004-12-31', '2004-09-30', '2004-06-30', '2004-03-31', '2003-12-31',
    #                       '2003-09-30', '2003-06-30', '2003-03-31', '2002-12-31', '2002-09-30', '2002-06-30',
    #                       '2002-03-31', '2001-12-31', '2001-06-30', '2000-12-31', '2000-06-30', '1999-12-31',
    #                       '1999-06-30', '1998-12-31', '1998-06-30', '1997-12-31', '1997-06-30', '1996-12-31',
    #                       '1995-12-31', '1994-12-31']
    # result = IncomeStatement.query_data(session=session, provider='eastmoney', return_type='domain',
    #                                     codes=['000778'], end_timestamp='2021-09-03',
    #                                     order=IncomeStatement.report_date.desc(), time_field='report_date')
    #
    # for item in result:
    #     print(item.code+':' + to_time_str(item.report_date)+'  financ cost:'+str(item.financing_costs)+'  net_profit:'+str(item.net_profit))

    #
    # latest: FinanceFactor = result[0]
    # latest1: FinanceFactor = result[-1]
    #
    # print('net_profit'+str(latest.net_profit))
    # print('-1'+'net_profit'+str(latest1.net_profit))
    # 归属净利润同比增长  无
    #print('net_profit_growth_yoy' + str(latest.net_profit_growth_yoy))
    #print('-1' + 'net_profit_growth_yoy' + str(latest1.net_profit_growth_yoy))
    # 扣非净利润同比增长  无
    #print('deducted_net_profit_growth_yoy' + str(latest.deducted_net_profit_growth_yoy))
    #print('-1' + 'deducted_net_profit_growth_yoy' + str(latest1.deducted_net_profit_growth_yoy))
    # 归属净利润滚动环比增长  无
    #print('net_profit_growth_qoq' + str(latest.net_profit_growth_qoq))
    #print('-1' + 'net_profit_growth_qoq' + str(latest1.net_profit_growth_qoq))
    # 扣非净利润滚动环比增长  无
    #print('deducted_net_profit_growth_qoq' + str(latest.deducted_net_profit_growth_qoq))
    #print('-1' + 'deducted_net_profit_growth_qoq' + str(latest1.deducted_net_profit_growth_qoq))

    # codes = []
    # start_timestamp = to_pd_timestamp(the_date) - datetime.timedelta(130)
    # 营收降，利润降,流动比率低，速动比率低
    # finance_filter = or_(FinanceFactor.op_income_growth_yoy < income_yoy,
    #                      FinanceFactor.net_profit_growth_yoy <= profit_yoy,
    #                      FinanceFactor.current_ratio < 0.7,
    #                      FinanceFactor.quick_ratio < 0.5)
    # df = FinanceFactor.query_data(entity_ids=entity_ids, start_timestamp=start_timestamp, filters=[finance_filter],
    #                               columns=['code'])