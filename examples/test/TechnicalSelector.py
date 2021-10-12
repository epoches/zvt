from zvt.contract import IntervalLevel
from zvt.factors.target_selector import TargetSelector
from zvt.factors.ma.ma_factor import CrossMaFactor
from zvt.factors import BullFactor
from zvt.domain import Stock
class TechnicalSelector(TargetSelector):

    def __init__(self, entity_ids=None, entity_type='stock', exchanges=['sh', 'sz'], codes=None,entity_schema = Stock,
                 the_timestamp=None, start_timestamp=None, end_timestamp=None, long_threshold=0.8, short_threshold=-0.8,
                 level=IntervalLevel.LEVEL_1DAY,
                 provider='joinquant') -> None:

        super().__init__(entity_ids, entity_type, exchanges, codes, the_timestamp, start_timestamp, end_timestamp,
                         long_threshold, short_threshold, level, provider)

    def init_factors(self, entity_ids, entity_type, exchanges, codes, the_timestamp, start_timestamp,
                     end_timestamp):
        bull_factor = BullFactor(entity_ids=entity_ids, entity_type=entity_type, exchanges=exchanges,
                                 codes=codes, the_timestamp=the_timestamp, start_timestamp=start_timestamp,
                                 end_timestamp=end_timestamp, provider=self.provider, level=self.level)

        self.filter_factors = [bull_factor]

if __name__ == '__main__':
    s = TechnicalSelector(codes='000338', start_timestamp='2018-01-01', end_timestamp='2019-06-30')
    s.run()
    s.draw()