import requests
from bs4 import BeautifulSoup
import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient-basic-windows.x64-21.9.0.0.0dbru\instantclient_21_9")
conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')

print('')
print('DB connect 성공!!')
print('')

cs = conn.cursor()

sql_get = """  SELECT * FROM clien_test_table1
                    WHERE ROWNUM =1 """   
cs.execute(sql_get)
head_rows = cs.fetchall()

url= ""
title=""
count = ""
date=""
write=""
id=""


count=1

for i in head_rows:
    if count == 1:
        url     = i[0]
        title   = i[1]
        count   = i[2]
        date    = i[3]
        write   = i[4]
        id      = i[5]
        count = 0
    else:
        break


sql_head = """  insert into head_table1 (CODE_URL,DATA_TITLE,DATA_COUNT,DATE_WRITE, EXTRACT_DATE,id) 
                VALUES (:CODE_URL,:DATA_TITLE,:DATA_COUNT,:DATE_WRITE,:EXTRACT_DATE,:id)
                """
cs.execute(sql_head,CODE_URL=url,DATA_TITLE=title,DATA_COUNT=count,DATE_WRITE=write, EXTRACT_DATE=date,id=id)

cs.close() 
conn.commit()
conn.close()

print(head_rows)