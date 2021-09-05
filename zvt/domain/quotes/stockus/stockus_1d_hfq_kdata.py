# -*- coding: utf-8 -*-
# this file is generated by gen_kdata_schema function, dont't change it
from sqlalchemy.orm import declarative_base

from zvt.contract.register import register_schema
from zvt.domain.quotes import StockusKdataCommon

KdataBase = declarative_base()


class Stockus1dHfqKdata(KdataBase, StockusKdataCommon):
    __tablename__ = 'stockus_1d_hfq_kdata'


register_schema(providers=['em'], db_name='stockus_1d_hfq_kdata', schema_base=KdataBase, entity_type='stockus')

# the __all__ is generated
__all__ = ['Stockus1dHfqKdata']