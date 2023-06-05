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

def db_delete_sub_title():
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    print('')
    print('DB connect 성공!!')
    print('')

    cs = conn.cursor()
    
    sql = "DELETE FROM SUB_TITLE"

    cs.execute(sql)
    
    deleted_rows = cs.rowcount
    print(f"{deleted_rows} rows deleted")
    
    cs.close()
    conn.commit()
    conn.close()

#-----------------------------------------------------------------------------------------#
def cleansing_sentence(input_string):
    string_pattern = re.compile(r'[^ㄱ-힣 0-9 a-z A-Z]')
    cleansing_string = string_pattern.sub('', input_string)
    return cleansing_string
#-----------------------------------------------------------------------------------------#

# 스크롤 제한적 실행
def scroll2():
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    for i in range(2): # 스크롤 횟수 지정
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        #time.sleep(1.5)
        time.sleep(1)

        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height



#sub_TABLE을 통해 얻어진 MAIN_KEYWORD + SUB_KEYWORD 한 문자로 출력 => 함수 내에서 사용
def sub_select():
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    cs = conn.cursor()
    # select_sub = 'SELECT * FROM SUB_KEYWORD'
    select_com = "SELECT MAIN_K || ' ' || SUB_K FROM SUB_KEYWORD"
    cs.execute(select_com)
    SUB_MAIN_C = cs.fetchall()
    
    cs.close()
    conn.close()
    return SUB_MAIN_C

# DB 저장 함수(크롤링 추출 자료 INSET)
def sub_title(KEYWORD, TITLE): 
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    print('')
    print('DB connect 성공!!')
    print('')

    cs = conn.cursor()
    
    sql = "INSERT INTO SUB_TITLE (MAINSUB_K, TITLE) VALUES (:1, :2)"

    cs.execute(sql, (KEYWORD, TITLE))
    cs.close()
    conn.commit()
    conn.close()

#MAIN_KEYWORD + SUB_KEYWORD 한 문자를 통한 크롤링
def get_sub_main():
    sub = sub_select()
    for i in range(len(sub)):
        keyword = sub[i][0]
        get_data_keyword(keyword)

#---------------------------------------------------------------------------------------------------------------------#
#keyword를 통해서 크롤링 => 반복문 안에 존재하면 효과적일듯
def get_data_keyword(keyword):

    #URL 지정
    URL = f"https://www.youtube.com/results?search_query={quote(keyword)}"

    #URL 실행
    driver.get(URL)
    sleep(3)
    #필터 버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="container"]/ytd-toggle-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]').click()
    sleep(1)
    
    #이번 달
    upload_date = driver.find_element(By.XPATH,'//*[@id="collapse-content"]/ytd-search-filter-group-renderer[1]')
    click_list_1 = upload_date.find_elements(By.ID,"endpoint")
    click_list_1[3].click()
    sleep(1)

    driver.find_element(By.XPATH, '//*[@id="container"]/ytd-toggle-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]').click()
    length = driver.find_element(By.XPATH,'//*[@id="collapse-content"]/ytd-search-filter-group-renderer[3]')
    click_list_2 = length.find_elements(By.ID,"endpoint")
    click_list_2[1].click()
    sleep(1)
    # scroll2()
    
    # 페이지 소스 추출
    html_source = driver.page_source
    soup_source = BeautifulSoup(html_source, 'html.parser')
    
    # 콘텐츠 모든 정보
    content_total = soup_source.find_all(class_ = 'yt-simple-endpoint style-scope ytd-video-renderer')
    
    # 콘텐츠 제목만 추출
    content_total_title = list(map(lambda data: data.get_text().replace("\n", ""), content_total))
    i = 0
    for title in content_total_title:
        title = cleansing_sentence(content_total_title[i])
        sub_title(keyword , title)
        print(keyword)
        print("제목 : ",title)
        print("-----------------------------------------------")
        i = i + 1


if __name__ == '__main__':
    cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient-basic-windows.x64-21.9.0.0.0dbru\instantclient_21_9")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    service = Service(ChromeDriverManager().install())

    ##sub_main문자를 들고 와서 크롤링후 sub_title테이블에 저장
    db_delete_sub_title()
    get_sub_main()
