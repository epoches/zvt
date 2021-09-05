# -*- coding: utf-8 -*-
import logging
import time

#import eastmoneypy
from apscheduler.schedulers.background import BackgroundScheduler

from examples.reports import stocks_with_info
from zvt import init_log, zvt_config
from zvt.contract.api import get_entities
from zvt.domain import Stock, Stock1dHfqKdata
from zvt.factors import BullFactor, CrossMaVolumeFactor
from zvt.factors.target_selector import TargetSelector
from zvt.informer.informer import EmailInformer

from typing import List

import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash import dash
from dash.dependencies import Input, Output, State

from zvt.api.trader_info_api import AccountStatsReader, OrderReader, get_order_securities
from zvt.api.trader_info_api import get_trader_info
from zvt.contract import Mixin
from zvt.contract import zvt_context, IntervalLevel
from zvt.contract.api import get_entities, get_schema_by_name, get_schema_columns
from zvt.contract.drawer import StackedDrawer
from zvt.domain import TraderInfo
from zvt.ui import zvt_app
from zvt.ui.components.dcc_components import get_account_stats_figure
from zvt.utils import pd_is_not_null

import pandas as pd
import numpy as np
import talib as ta

from matplotlib import rc
rc('mathtext', default='regular')
import seaborn as sns
sns.set_style('white')
#%matplotlib inline
import matplotlib  # 注意这个也要import一次

import matplotlib.pyplot as plt

#return_type='domain'
#,order=Stock1dHfqKdata.timestamp.desc(), limit=1
#sh sz 股票
#return_type domain dict
#证券类型(entity_type)  股票(stock) 交易所(exchange) 上海证券交易所(sh)，深圳证券交易所(sz) 代码(code) A股中的000338
#唯一编码(entity_id)为:{entity_type}\_{exchange}\_{code}


#获取所有schemas global_schemas就是系统支持的所有数据，具体含义可以查看相应字段的注释
# schemas = zvt_context.entity_map_schemas.get('stock')
# for schema in schemas:
#     print('schemas'+str(schema))



dw = Stock1dHfqKdata.query_data(provider='joinquant', entity_id='stock_sh_600563', return_type='dict',
                                                         start_timestamp='2016-01-18',end_timestamp = '2016-07-18')
#target_date = latest_day[0].timestamp
#print(target_date)
#print(latest_day[0].close)
#target_date = latest_day[0].close
dw['macd'], dw['macdsignal'], dw['macdhist'] = ta.MACD(dw.close, fastperiod=12, slowperiod=26, signalperiod=9)
dw[['close','macd','macdsignal','macdhist']].plot()
#for stock in dw:
    #print(str(stock.close)+str(stock.open))
    #print(stock.timestamp)
    #print(stock.code)
    #print(stock.name)