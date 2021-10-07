import matplotlib.pyplot as plt
import talib as ta
import pandas as pd
from zvt.utils import next_date, to_pd_timestamp
from zvt.domain import Stock, Stock1dHfqKdata,StockValuation,Stock1dKdata
from zvt.domain import FinanceFactor, BalanceSheet, Stock
from zvt.utils.time_utils import TIME_FORMAT_DAY, now_pd_timestamp
import seaborn as sns
sns.set_style('white')
plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False # 用来正常显示负号
codeid ='600745'
starttime ='2011-10-5'
endtime=now_pd_timestamp()
Stock1dKdata.record_data(provider='joinquant', code=codeid)
dw = Stock1dKdata.query_data(provider='joinquant',code=codeid, #entity_id='stock_sh_600563',
                                                         start_timestamp=starttime,end_timestamp = endtime)
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1) #得到fig对象之后，通过add_subplot增加子图（返回了一个axes坐标轴），该方法需要三个参数，分别为：numrows, numcols, fignum。其中，一共有numrows*numcols个子图，即：将图表分为N行*M列，fignum标识了该子图的顺序，其范围从1到numrows*numcols。在上例中1,1,1表示了该绘图对象仅有1个子图，也就是1*1类型。

fig.suptitle('pe-band测试', fontsize = 14, fontweight='bold')
ax1.set_title(dw.loc[0,'name']+"收盘价")
ax1.set_xlabel("时间")
ax1.set_ylabel("价格")
#plt.gca().xaxis.set_major_formatter(dw['timestamp'].DateFormatter('%Y-%m'))  #設置x軸主刻度顯示格式（日期）
#plt.gca().xaxis.set_major_locator(dw.MonthLocator(interval=15))  #設置x軸主刻度間距
#,columns=FinanceFactor.important_cols()
FinanceFactor.record_data(code=codeid)
df = FinanceFactor.query_data(code=codeid,index='timestamp',
                              filters=[FinanceFactor.report_period == 'half_year'],
                              start_timestamp=starttime,end_timestamp = endtime)
#print(df)
StockValuation.record_data(code=codeid)
dfvaluation = StockValuation.query_data(code=codeid,index='timestamp',
                              start_timestamp=starttime,end_timestamp = endtime)

plt.subplots_adjust(bottom=0.13, top=0.95)
dfvaluation['eps']=df['basic_eps']

# df2=dfvaluation.copy(deep=True)

#获取历史最高价和最低价 ，确定五个相等间隔的市盈率
#计算pb，每股净资产bps
pe = dfvaluation.iloc[0,10]
if pe<0:
    pe=0
pettmmax = dfvaluation.loc[dfvaluation['pe'].idxmax(),'pe']
pettmmin = dfvaluation.loc[dfvaluation['pe'].idxmin(),'pe']
pettmdiv = (pettmmax-pettmmin)/5
pe1=pettmmin+pettmdiv
if pe1<0:
    pe1=0
pe2=pettmmin+pettmdiv*2
pe3=pettmmin+pettmdiv*3
pe4=pettmmin+pettmdiv*4
pe5=pettmmin+pettmdiv*5
oldtime='1980-01-01'
for dfitem in df['timestamp']:
    for dfvitem in dfvaluation['timestamp']:
        if (dfvaluation['timestamp'].between(oldtime,dfitem).loc[dfvitem]):
            pettm = dfvaluation.loc[dfvaluation['timestamp'] == dfvitem, 'pe_ttm'][0]
            #获取pe_ttm，进行计算
            #s = df.iloc[df.index.get_loc(dfvitem,method='nearest')]
            #eps = s['basic_eps']
            eps=df.loc[dfitem,'basic_eps']
            if eps<0:
                eps=0
            dfvaluation.loc[dfvaluation['timestamp'] == dfvitem,'df1']=eps*pe1
            dfvaluation.loc[dfvaluation['timestamp'] == dfvitem,'df2'] = eps*pe2
            dfvaluation.loc[dfvaluation['timestamp'] == dfvitem,'df3'] = eps*pe3
            dfvaluation.loc[dfvaluation['timestamp'] == dfvitem,'df4'] = eps*pe4
            dfvaluation.loc[dfvaluation['timestamp'] == dfvitem,'df5'] = eps*pe5
            dfvaluation.loc[dfvaluation['timestamp'] == dfvitem, 'df6'] = eps * pettm
    oldtime=dfitem


print(dfvaluation)

ax1.plot(dw['timestamp'],dw['close'])
ax1.plot(dfvaluation['timestamp'],dfvaluation['df1'])
ax1.plot(dfvaluation['timestamp'],dfvaluation['df2'])
ax1.plot(dfvaluation['timestamp'],dfvaluation['df3'])
ax1.plot(dfvaluation['timestamp'],dfvaluation['df4'])
ax1.plot(dfvaluation['timestamp'],dfvaluation['df5'])
ax1.plot(dfvaluation['timestamp'],dfvaluation['df6'])
#ax1.plot(dfvaluation['timestamp'],dfvaluation['df1'],dfvaluation['df2'],dfvaluation['df3'],dfvaluation['df4'],dfvaluation['df5'])
plt.legend(('收盘价', pe1,pe2,pe3,pe4,pe5,'计算股价'))
plt.grid(True)

plt.show()