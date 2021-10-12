from zvt.factors import MaStatsFactor
codes = ['000338']
my_selector1 = MaStatsFactor(entity_ids=['stock_sh_600225'],
                             start_timestamp='2021-01-01', end_timestamp='2021-06-01')
long_targets = my_selector1.result_df
print(long_targets)