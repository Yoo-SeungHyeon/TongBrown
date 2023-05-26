import requests
from bs4 import BeautifulSoup
import cx_Oracle
import re

def cleansing_sentence(input_string):
    string_pattern = re.compile(r'[^ㄱ-힣 0-9 a-z A-Z]')
    cleansing_string = string_pattern.sub('', input_string)
    return cleansing_string


def url_parsing(response,url_code):
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        div = soup.select_one('div.dabate-type-list')

        titles = div.select('table > tbody > tr > td > p > a')
        counts = div.select('table > tbody > tr > td > span.count')
        date = div.select('table > tbody > tr > td > span.date')
        link = div.select('table > tbody > tr > td > p > a.subject-link')
        title_list =[]
    
        i=0

        for title in titles:
            title = cleansing_sentence(title.get_text())
            title_list.append(title.strip())
            counts[i] = counts[i].get_text().strip()
            date[i] = date[i].get_text().strip()
            link[i] = link[i].get('href')
            print("제목 : ",title_list[i])
            print("조회수 : ",counts[i])
            print("날짜 : ",date[i])
            print("링크 : ",link[i])
            print("-----------------------------------------------")
        
            i = i + 1
        db_insert(url_code,title_list, counts,date,link)

def db_insert(url_code,title_list, counts, date,link): # DB 저장 함수(크롤링 추출 자료 INSET)
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')

    print('')
    print('DB connect 성공!!')
    print('')

    cs = conn.cursor()
    sql = "INSERT INTO cBASIC_DATA (CODE_URL,DATA_TITLE,DATA_COUNT,DATE_WRITE, DATA_LINK,EXTRACT_DATE) VALUES (:1,:2,:3,:4,:5,TO_CHAR(SYSDATE,'YYYYMMDD'))"

    i = 0
    for title in title_list:
        cs.execute(sql, (url_code, title_list[i], counts[i],date[i],link[i]))
        i = i + 1

    print("[%d]건 INSERT 완료" % 30)
    cs.close()
    conn.commit()
    conn.close()


def re_url():
    for page in range(1,51):
        url2 = "https://quasarzone.com/bbs/qb_free?page={}".format(str(page))
        url_code = "02"
        response = requests.get(url2)
        url_parsing(response,url_code)
        print("\n\n\n\n\n\n",page)


if __name__ == '__main__':
    cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient-basic-windows.x64-21.9.0.0.0dbru\instantclient_21_9")
    re_url()
