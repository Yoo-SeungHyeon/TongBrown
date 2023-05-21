import cx_Oracle
import requests
from bs4 import BeautifulSoup

url = "https://quasarzone.com/bbs/qb_tsy"  # 크롤링 대상 URL
url_code = "01"  # 해당 URL 코드(URL_LIST.CODE_URL)

def url_parsing(): # 크롤링 함수
    # requests를 이용하여 URL의 HTML 문서를 가져옴
    response = requests.get(url)

    # URL 접속이 되지 않으면 실행되지 않는다.
    if response.status_code == 200: # 정상 상태코드(200)
        soup = BeautifulSoup(response.text, "html.parser")

        # 해당 URL 추출 data를 구분한다.
        div = soup.select_one('div.market-type-list')

        titles = div.select('div > div > p > a > span.ellipsis-with-reply-cnt')
        prices = div.select('div > div.list-board-wrap > div.market-type-list.market-info-type-list.relative > table > tbody > tr > td > div > div > div > p > span > span')
        counts = div.select('div > div.list-board-wrap > div.market-type-list.market-info-type-list.relative > table > tbody > tr> td > div > div > div > p > span.count')
        links = div.select("a", class_="subject-link")

        i = 0

        for title in titles:
            print("제목 : " + title.get_text())
            print("조회수 : " + counts[i].get_text().strip())
            print("가격 : " + prices[i].get_text().strip())
            print("링크 " + links[i].get('href'))
            print('-------------------------------------------------------------------------')
            i=i+1

        db_insert(titles, prices, counts, links)

    else:
        print(response.status_code)

def db_insert(titles, prices, counts, links): # DB 저장 함수(크롤링 추출 자료 INSET)
    cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient-basic-windows.x64-21.9.0.0.0dbru\instantclient_21_9")
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')

    print('')
    print('DB connect 성공!!')
    print('')

    cs = conn.cursor()
    sql = "INSERT INTO BASIC_DATA (CODE_URL,DATA_TITLE,DATA_COUNT,DATA_PRICE,DATA_LINK,DATE_WRITE) VALUES (:1,:2,:3,:4,:5,TO_CHAR(SYSDATE,'YYYYMMDD'))"

    i = 0
    for title in titles:
        cs.execute(sql, (url_code,title.get_text(), counts[i].get_text().strip(), prices[i].get_text().strip(),links[i].get('href')))
        i = i + 1

    print("[%d]건 INSERT 완료" % 30)
    cs.close()
    conn.commit()
    conn.close()


# 메인 함수(항상 가장 먼저 실행된다.)
if __name__ == '__main__':
    url_parsing()
