from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import quote
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import time
import random
import cx_Oracle
import re
from selenium.webdriver.chrome.service import Service
from openpyxl import Workbook
from selenium.common.exceptions import ElementNotInteractableException ## 추가됨
from selenium.common.exceptions import NoSuchElementException ## 추가됨
import sys ## 추가됨
import pandas as pd ##추가됨

def db_delete_detail_keyword():
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    print('')
    print('DB connect 성공!!')
    print('')

    cs = conn.cursor()
    
    sql = "DELETE FROM DETAIL_KEYWORD"

    cs.execute(sql)
    
    deleted_rows = cs.rowcount
    print(f"{deleted_rows} rows deleted")
    
    cs.close()
    conn.commit()
    conn.close()

#main+sub문자를 통해 크롤링한 title을 db에 저장
def select_sub_title():
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    cs = conn.cursor()
    select_sub_title = "SELECT * FROM SUB_TITLE"
    cs.execute(select_sub_title)
    title = cs.fetchall()

    cs.close()
    conn.close()
# 분석을 통해 dataframe을 받으면 detail_keyword에 저장 
def df_insert_detail(df):
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    cs = conn.cursor()
    insert_sql = 'INSERT INTO DETAIL_KEYWORD (MAINSUB_K, DET_K) VALUES(:1, :2)'
    for i in range(len(df)):
        main_sub = df.iloc[i][0]
        detail_keyword = df.iloc[i][1]
        cs.execute(insert_sql, (main_sub, detail_keyword))
        
    cs.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient-basic-windows.x64-21.9.0.0.0dbru\instantclient_21_9")
    db_delete_detail_keyword()
    
    #sub_title 들고옴
    select_sub_title()

    ## 분석 ##
    print("분석중")
    #분석결과
    # dataframe제작
    main_sub = ["경제 위기","경제 위기","경제 위기"]
    detail_keyword = ["한국", "영국", "미국"]
    df = pd.DataFrame({'main_sub' : main_sub, 'detail_keyword' : detail_keyword})

    df_insert_detail(df)

    #분석결과를 dataframe으로 받게 되면 detail_keyword에 저장