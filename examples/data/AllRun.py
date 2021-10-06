import os
lst = os.listdir(os.getcwd())

for c in lst:
    if os.path.isfile(c) and c.endswith('.py') and c.find("AllRun")==-1 and c.find("__init__")== -1:  # 去掉AllRun.py文件
        print(c)
        os.system("#nohup python3 ./%s & " % c)
