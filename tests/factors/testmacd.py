# -*- coding: utf-8 -*-
from zvt.contract import IntervalLevel
from zvt.factors.algorithm import MaTransformer, MacdTransformer
from zvt.factors.ma.ma_factor import CrossMaFactor
from ..context import init_test_context

init_test_context()

from zvt.factors.technical_factor import TechnicalFactor


from jqdatasdk import *
auth('13956782345','Yjbir=1977')

def test_macd():
    print(get_query_count())
    factor = TechnicalFactor(provider='joinquant', codes=['000338'], start_timestamp='2021-05-01',
                             end_timestamp='2021-08-30', level=IntervalLevel.LEVEL_1DAY, computing_window=None,
                             transformer=MacdTransformer(), adjust_type='qfq')


    print(factor.factor_df.tail())

    # compare with east money manually
    diff = factor.factor_df['diff']
    dea = factor.factor_df['dea']
    macd = factor.factor_df['macd']

    assert round(diff.loc[('stock_sz_000338', '2021-08-10')], 2) == 0.72



