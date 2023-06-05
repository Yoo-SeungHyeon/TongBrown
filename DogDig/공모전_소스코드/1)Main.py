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
#-----------------------------------------------------------------------------------------#
#youtube_table삭제
def db_delete_main():
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    print('')
    print('DB connect 성공!!')
    print('')

    cs = conn.cursor()
    
    sql = "DELETE FROM MAIN_TITLE"
    sql2 = "DELETE FROM MAIN_KEYWORD"
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
def db_insert(title,link): # DB 저장 함수(크롤링 추출 자료 INSET)
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    print('')
    print('DB connect 성공!!')
    print('')

    cs = conn.cursor()
    
    ## sql = "INSERT INTO YOUTUBE_TABLE (TITLE,LINK) VALUES (:1, :2)"
    sql = "INSERT INTO MAIN_TITLE (MAIN_K,TITLE) VALUES (:1, :2)"

    cs.execute(sql, (title,link))
    
    print("INSERT 완료")
    cs.close()
    conn.commit()
    conn.close()
#-----------------------------------------------------------------------------------------#
def cleansing_sentence(input_string):
    string_pattern = re.compile(r'[^ㄱ-힣 0-9 a-z A-Z]')
    cleansing_string = string_pattern.sub('', input_string)
    return cleansing_string
#-----------------------------------------------------------------------------------------#
def scroll():
    try:       
        # 페이지 내 스크롤 높이 받아오기
        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            # 임의의 페이지 로딩 시간 설정
            # PC환경에 따라 로딩시간 최적화를 통해 scraping 시간 단축 가능
            pause_time = random.uniform(1, 2)
            # 페이지 최하단까지 스크롤
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            # 페이지 로딩 대기
            time.sleep(pause_time)
            # 무한 스크롤 동작을 위해 살짝 위로 스크롤(i.e., 페이지를 위로 올렸다가 내리는 제스쳐)
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight-50)")
            time.sleep(pause_time)
            # 페이지 내 스크롤 높이 새롭게 받아오기
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
            # 스크롤을 완료한 경우(더이상 페이지 높이 변화가 없는 경우)
            if new_page_height == last_page_height:
                print("스크롤 완료")
                break
                
            # 스크롤 완료하지 않은 경우, 최하단까지 스크롤
            else:
                last_page_height = new_page_height
            
    except Exception as e:
        print("에러 발생: ", e)

#MAIN_KEWORD에 MAIN_K 넣는 명령어 => 첫 MAIN키워드 크롤링시 사용
def insert_main(keyword):
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    cs = conn.cursor()
    sql_insert = 'INSERT INTO MAIN_KEYWORD (MAIN_K) VALUES (:1)'

    cs.execute(sql_insert, (keyword,))
    
    cs.close()
    conn.commit()
    conn.close()
#-----------------------------------------------------------------------------------------------------------------#

#title 크롤링
def get_data():
    #원하는 검색어 입력받음
    main_k = input('원하는 검색을 입력하시오:')
    insert_main(main_k) # MAIN_KEYWORD 테이블에 MAIN_K저장
    #URL 지정
    URL = f"https://www.youtube.com/results?search_query={quote(main_k)}"

    #URL 실행
    driver.get(URL)

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
    # 무한 스크롤 함수 실행
    # scroll()

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
    
        db_insert(main_k,title)
        print("제목 : ",title)
        print("-----------------------------------------------")
        i = i + 1

if __name__ == '__main__':
    cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient-basic-windows.x64-21.9.0.0.0dbru\instantclient_21_9")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    service = Service(ChromeDriverManager().install())

    db_delete_main()  #유튜브_title테이블 삭제
    get_data() #MAIN_K를 입력하면 크롤링후 MAIN_TITLE 테이블에 저장.


    #1. 유튜브_TITLE테이블 삭제후 input을 통해 단어를 입력 받으면 크롤링후 테이블에 저장
    ## input문 존재 