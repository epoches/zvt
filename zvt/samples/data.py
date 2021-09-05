# -*- coding: utf-8 -*-
from zvt.contract import IntervalLevel
from zvt.factors.algorithm import MaTransformer, MacdTransformer
from zvt.factors.ma.ma_factor import CrossMaFactor
from zvt.domain import *
def getdata():
    Stock.record_data(provider='joinquant')
    # Stock.record_data(provider='eastmoney')
    # FinanceFactor.record_data(provider='joinquant')
    # BalanceSheet.record_data(provider='joinquant')
    # IncomeStatement.record_data(provider='joinquant')
    # CashFlowStatement.record_data(provider='joinquant')