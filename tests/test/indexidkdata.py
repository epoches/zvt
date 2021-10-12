
from zvt.domain import Index1dKdata

Index1dKdata.record_data(provider='sina')
df = Index1dKdata.query_data(provider='sina',codes=['000300'], return_type='df',
                             start_timestamp="2021-01-01", end_timestamp="2021-07-05")
print(df)