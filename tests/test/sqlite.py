import sqlite3
from ..context import init_test_context
init_test_context()
def test():
    conn = sqlite3.connect('C:\\Users\\PC\\zvt-home\\data\\joinquant_stock_1d_hfq_kdata.db')
    print("Opened database successfully")
    c = conn.cursor()
    cursor = c.execute("SELECT code,close  from stock_1d_hfq_kdata where code='000004'")
    results = cursor.fetchall()
    print(results)
    for item in results:
        print(item[0])
        print(item[1])
    # for row in cursor:
    #     print("CODE = ", row[0])
    #     print("NAME = ", row[1])
    #     print("CLOSE = ", row[2])
    print("Operation done successfully")
    conn.close()