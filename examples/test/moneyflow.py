from zvt.contract.factor import FilterFactor, ScoreFactor, Factor
from zvt.domain import IndexMoneyFlow, Index, StockMoneyFlow
from typing import Union, Type
from typing import List
import pandas as pd
from zvt.contract import AdjustType
from zvt.contract import IntervalLevel
from zvt.factors import RankScorer,QuantileScorer
from zvt.contract.factor import Scorer, Transformer
from zvt.factors.target_selector import TargetSelector
from zvt.api import *

class IndexMoneyFlowFactor(ScoreFactor):
    def __init__(self,
                 the_timestamp: Union[str, pd.Timestamp] = None,
                 start_timestamp: Union[str, pd.Timestamp] = None,
                 end_timestamp: Union[str, pd.Timestamp] = None,
                 columns: List = [IndexMoneyFlow.net_inflows, IndexMoneyFlow.net_inflow_rate,
                                  IndexMoneyFlow.net_main_inflows, IndexMoneyFlow.net_main_inflow_rate],
                 filters: List = None,
                 order: object = None,
                 limit: int = None,
                 provider: str = 'sina',
                 level: Union[str, IntervalLevel] = IntervalLevel.LEVEL_1DAY,
                 category_field: str = 'entity_id',
                 time_field: str = 'timestamp',
                 trip_timestamp: bool = True,
                 auto_load: bool = True,
                 keep_all_timestamp: bool = False,
                 fill_method: str = 'ffill',
                 effective_number: int = 10,
                 scorer: Scorer = RankScorer(ascending=True)) -> None:
        super().__init__(IndexMoneyFlow, None, 'index', None, None, the_timestamp, start_timestamp,
                         end_timestamp, columns, filters, order, limit, provider, level, category_field, time_field,
                         trip_timestamp, auto_load, keep_all_timestamp, fill_method, effective_number, scorer)

    def pre_compute(self):
        self.depth_df = self.data_df.copy()
        self.depth_df = self.depth_df.groupby(level=1).rolling(window=20).mean()
        self.depth_df = self.depth_df.reset_index(level=0, drop=True)
        self.depth_df = self.depth_df.reset_index()
        self.depth_df = index_df_with_category_xfield(self.depth_df)

class RankScorer(Scorer):
    def __init__(self, ascending=True) -> None:
        self.ascending = ascending

    def compute(self, input_df) -> pd.DataFrame:
        result_df = input_df.groupby(level=1).rank(ascending=self.ascending, pct=True)
        return result_df

class IndexSelector(TargetSelector):

    def __init__(self, entity_ids=None, entity_type='stock', exchanges=['sh', 'sz'], codes=None, the_timestamp=None,
                 start_timestamp=None, end_timestamp=None, long_threshold=0.8, short_threshold=0.2,
                 level=IntervalLevel.LEVEL_1DAY, provider='sina', block_selector=None) -> None:
        super().__init__(entity_ids, entity_type, exchanges, codes, the_timestamp, start_timestamp, end_timestamp,
                         long_threshold, short_threshold, level, provider, block_selector)

    def init_factors(self, entity_ids, entity_type, exchanges, codes, the_timestamp, start_timestamp, end_timestamp,
                     level):
        index_factor = IndexMoneyFlowFactor(start_timestamp=start_timestamp, end_timestamp=end_timestamp, level=level,
                                            provider='sina', codes=codes)
        self.score_factors.append(index_factor)

if __name__ == '__main__':
    df = get_blocks(provider='sina', block_category='industry')
    index_selector = IndexSelector(entity_type='index', exchanges=None, start_timestamp='2019-01-01',
                                       end_timestamp=now_pd_timestamp(), codes=df['code'].to_list())
    index_selector.run()