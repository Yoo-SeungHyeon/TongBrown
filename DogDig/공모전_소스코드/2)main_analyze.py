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

def db_delete_sub_keyword():
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    print('')
    print('DB connect 성공!!')
    print('')

    cs = conn.cursor()
    
    sql = "DELETE FROM SUB_KEYWORD"

    cs.execute(sql)
    
    deleted_rows = cs.rowcount
    print(f"{deleted_rows} rows deleted")
    
    cs.close()
    conn.commit()
    conn.close()

def select_main_title():
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    cs = conn.cursor()

    select_sql = "SELECT TITLE FROM MAIN_TITLE"
    cs.execute(select_sql)
    main_title = cs.fetchall()


    cs.close()
    conn.close()

    return main_title

#MAIN_KEYWORD테이블에서 MAIN_K 찾기 => 함수내에서 사용
def select_main():
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    cs = conn.cursor()
    select_main_keyword= 'select MAIN_K from MAIN_KEYWORD'
    cs.execute(select_main_keyword)
    
    main_keyword = cs.fetchall()
    cs.close()
    conn.close()
    return main_keyword

#SUB_KEYWORD테이블에 MAIN_KEYWORD,  SUB_KEYWORD넣기 #지워도 될듯
def sub_insert(main_keyword, sub_keyword):
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    cs = conn.cursor()
    insert_sub_keyword = 'INSERT INTO SUB_KEYWORD (MAIN_k, SUB_k) VALUES(:1, :2)'
    cs.execute(insert_sub_keyword,(main_keyword, sub_keyword))
    
    cs.close()
    conn.commit()
    conn.close()

#SUB_KEYWORD넣기 자동화 => 분석을 통해 찾는 SUB_KEYWORD리스트를 넣기만 하면됨 #지워도 될듯
def sub_insert2(sub_keyword_list):
    main_keyword = select_main()
    main_keyword = main_keyword[0][0]
    for sub_keyword in sub_keyword_list:
        sub_insert(main_keyword, sub_keyword)
###########################################
# 분석을 통해 dataframe을 받으면 SUB_KEYWORD에 저장 
def df_insert_sub(df):
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    cs = conn.cursor()
    insert_sql = 'INSERT INTO SUB_KEYWORD (MAIN_K, SUB_K) VALUES(:1, :2)'
    for i in range(len(df)):
        main_k = df.iloc[i][0]
        sub_keyword = df.iloc[i][1]
        cs.execute(insert_sql, (main_k, sub_keyword))
        
    cs.close()
    conn.commit()
    conn.close()
####################################
if __name__ == '__main__':
    cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient-basic-windows.x64-21.9.0.0.0dbru\instantclient_21_9")
    
    
    db_delete_sub_keyword()
    main_title = select_main_title()
    #분석
    print("분석중")

    # dataframe제작
    main_k= ["경제","경제","경제"]
    sub_keyword = ["한국", "미국", "영국"]
    df = pd.DataFrame({'main_sub' : main_k, 'detail_keyword' : sub_keyword})

    df_insert_sub(df)
    #크롤링을 통해 분석 결과를 dataframe으로 받게 되면 sub_keyword테이블에 저장됨