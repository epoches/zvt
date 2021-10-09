from jqdatasdk import *
auth('19159862375', 'Yjbir=1977')
#auth('18055893968', 'Yjbir=1977')
#auth('13956782345', 'Yjbir=1977')

# 查询当日剩余可调用数据条数
count = get_query_count()
print(count)