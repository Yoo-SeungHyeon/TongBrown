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

        div = soup.select_one('div.list_content')

        titles = div.select('div > div > a > span.subject_fixed')
        counts = div.select('div > div > span.hit')
        date = div.select('div > div > span > span.timestamp')
        # link = div.select('div >div > a.list_subject')
        title_list =[]
    
        i=0
        for title in titles:
            title = cleansing_sentence(title.get_text())
            title_list.append(title.strip())
            counts[i] = counts[i].get_text().strip()
            date[i] = date[i].get_text().strip()
            #link[i] = link[i].get('href')
            print("제목 : ",title_list[i])
            print("조회수 : ",counts[i])
            print("날짜 : ",date[i])
            #print("링크 : ",link[i])
            print("-----------------------------------------------")
        
            i = i + 1
        #db_insert(url_code,title_list, counts,date,link)
        db_insert(url_code,title_list, counts,date)

def db_insert(url_code,title_list, counts, date): # DB 저장 함수(크롤링 추출 자료 INSET)
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')

    print('')
    print('DB connect 성공!!')
    print('')

    cs = conn.cursor()

    
    sql_get1 = """  SELECT * FROM head_table1
                    WHERE ROWNUM =1 """   
    cs.execute(sql_get1)
    head_rows1 = cs.fetchone()
   
    sql = "INSERT INTO clien_test_table1 (CODE_URL,DATA_TITLE,DATA_COUNT,DATE_WRITE, EXTRACT_DATE,id) VALUES (:1,:2,:3,:4,TO_CHAR(SYSDATE,'YYYYMMDD'),clien_sequence.NEXTVAL)"

    i = 0
    for title in title_list:
        if head_rows1[1] != title:
            cs.execute(sql, (url_code, title_list[i], counts[i],date[i]))
            i = i + 1
        else:
            break
        
    print("[%d]건 INSERT 완료" % 30)
    cs.close()
    conn.commit()
    conn.close()

def re_url():
    for page in range(3,10):
        url2 = "https://www.clien.net/service/board/cm_stock?&od=T31&category=0&po={}".format(str(page))
        url_code = "03"
        response = requests.get(url2)
        url_parsing(response,url_code)
        print("\n\n\n\n\n\n",page)

if __name__ == '__main__':
    cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient-basic-windows.x64-21.9.0.0.0dbru\instantclient_21_9")
    re_url()