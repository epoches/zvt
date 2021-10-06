import os
from datetime import datetime
import time
#每隔n秒执行一次
time.sleep(10800)
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
os.system("python3 /home/epoches/zvt/examples/recorders/AllRun.py")