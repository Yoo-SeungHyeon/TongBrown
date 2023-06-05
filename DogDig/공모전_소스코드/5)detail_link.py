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

def db_delete_detail_link_script():
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    print('')
    print('DB connect 성공!!')
    print('')

    cs = conn.cursor()
    
    sql = "DELETE FROM DETAIL_LINK"
    sql2 = "DELETE FROM SCRIPT_TABLE"
    cs.execute(sql)
    
    deleted_rows = cs.rowcount
    print(f"{deleted_rows} rows deleted")

    cs.execute(sql2)
    
    deleted_rows2 = cs.rowcount
    print(f"{deleted_rows2} rows deleted")

    
    cs.close()
    conn.commit()
    conn.close()
#-----------------------------------------------------------------------------------------#
def cleansing_sentence(input_string):
    string_pattern = re.compile(r'[^ㄱ-힣 0-9 a-z A-Z]')
    cleansing_string = string_pattern.sub('', input_string)
    return cleansing_string
#스크립 효과음 제거
def clean_sent(input_string):
    string_pattern = re.compile(r'\[[ㄱ-힣][ㄱ-힣]\]')
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
def detail_insert(keyword, link):
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    cs = conn.cursor()

    insert_detail = "INSERT INTO DETAIL_LINK (DET_K, LINK) VALUES (:1, :2)"
    cs.execute(insert_detail,(keyword, link))

    cs.close()
    conn.commit()
    conn.close()

# main_sub_detail keyword를 한번에 들고오는 함수
def select_detail():
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    cs = conn.cursor()
    select_detail = "SELECT MAINSUB_K || ' ' || DET_K FROM DETAIL_KEYWORD"
    cs.execute(select_detail)
    main_sub_detail = cs.fetchall()


    cs.close()
    conn.commit()
    conn.close()
    return main_sub_detail

#MAIN_KEYWORD + SUB_KEYWORD 한 문자를 통한 크롤링
def get_detail():
    sub = select_detail()
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
    
    # 콘텐츠 링크만 추출
    content_total_link = list(map(lambda data: "https://youtube.com" + data["href"], content_total))


    i = 0
    for links in content_total_link:
        link = content_total_link[i]
        detail_insert(keyword, link)
        print(keyword)
        print("링크 : ",link)
        print("-----------------------------------------------")
        i = i + 1

def comment():
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    cs = conn.cursor()
    ## sql = "SELECT LINK FROM YOUTUBE_TABLE"
    sql = "SELECT LINK FROM DETAIL_LINK FETCH FIRST 200 ROWS ONLY"
    sql_insert = "INSERT INTO SCRIPT_TABLE (LINK, SCRIPT) VALUES (:1,:2)"
    cs.execute(sql)
    links = cs.fetchall()
    # print(links)
    for link in links:
        URL = link[0]
            #URL 실행
        driver.get(URL)

        wb = Workbook(write_only=True)
        ws = wb.create_sheet()

        driver.implicitly_wait(5)

        time.sleep(1.5)

        driver.find_element(By.XPATH, '//*[@id="button-shape"]/button/yt-touch-feedback-shape/div').click()
        time.sleep(1)
        try:
            driver.find_element(By.XPATH, '//*[@id="items"]/ytd-menu-service-item-renderer[1]/tp-yt-paper-item').click()
            time.sleep(1)
        except NoSuchElementException:
            continue
        except ElementNotInteractableException:
            continue
        
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')

         #-------------------------------------------------------------------------------------------#
        scipt_html = soup.find_all('yt-formatted-string', class_='segment-text style-scope ytd-transcript-segment-renderer')
        
        for i in range(len(scipt_html)):
            temp_comment = scipt_html[i].text
            temp_comment = clean_sent(temp_comment)
            print(temp_comment)

            cs.execute(sql_insert, (URL, temp_comment))
            if i % 50 == 0:
               conn.commit() 
        #-------------------------------------------------------------------------------------------#
    cs.close()
    conn.commit()
    conn.close()
#----------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient-basic-windows.x64-21.9.0.0.0dbru\instantclient_21_9")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    service = Service(ChromeDriverManager().install())
    
    db_delete_detail_link_script()
    get_detail()
    comment()

    #detail_keyword로 검색된 detail_link를 크롤링함
    #크롤링후 스크립까지 가져오는 알고리즘 