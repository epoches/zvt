from jqdatasdk import *

auth('13956782345', 'Yjbir=1977')

# 查询当日剩余可调用数据条数
count = get_query_count()
print(count)