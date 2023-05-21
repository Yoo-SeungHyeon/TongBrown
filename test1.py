import cx_Oracle
import requests
from bs4 import BeautifulSoup

url2 = "https://quasarzone.com/bbs/qb_free" 
url_code = "02" 

def url_parsing(): 
    response2 = requests.get(url2)

    if response2.status_code == 200: 
        soup = BeautifulSoup(response2.text, "html.parser")

        div = soup.select_one('div.dabate-type-list')

        titles = div.select('table > tbody > tr > td > p > a')
        days = div.select('table > tbody > tr > td > span.date')
        counts = div.select('table > tbody > tr > td > span.count')
        links = div.select("a", class_="subject-link")

        i = 0

        for title in titles:
            print("제목 : " + title.get_text().strip())
            print("조회수 : " + counts[i].get_text().strip())
            print("날짜 : " + days[i].get_text().strip())
            print("링크 " + links[i].get('href'))
            print('-------------------------------------------------------------------------')
            i=i+1
            
        db_insert(titles, days, counts, links)
    else:
        print(response.status_code)

def db_insert(titles, days, counts, links): # DB 저장 함수(크롤링 추출 자료 INSET)
    cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient-basic-windows.x64-21.9.0.0.0dbru\instantclient_21_9")
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')

    print('')
    print('DB connect 성공!!')
    print('')

    cs = conn.cursor()
    sql = "INSERT INTO TONG_BROWN_RAW (CODE_URL, DATA_TITLE, DATA_COUNT, DATA_LINK, DATA_WRITE) VALUES (:1,:2,:3,:4,:5)"

    i = 0
    
    for title in titles:
        cs.execute(sql, (url_code, title.get_text().strip(), counts[i].get_text().strip(), links[i].get('href'), days[i].get_text().strip()))
        i = i + 1

    print("[%d]건 INSERT 완료" % 30)
    cs.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    url_parsing()