import cx_Oracle

url_code = "01"  # 해당 URL 코드(URL_LIST.CODE_URL)

def db_remake():
    cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient-basic-windows.x64-21.9.0.0.0dbru\instantclient_21_9")
    conn = cx_Oracle.connect(user='admin', password='Tongbrown@23', dsn='tongbrown_high')
    print('')
    print('  DB connect 성공!!')
    print('')

    cs = conn.cursor()

    # SELECT 쿼리 작성
    select_sql = "SELECT DATA_TITLE,DATA_LINK FROM BASIC_DATA WHERE CODE_URL = :1"

    # URL_LIST.CODE_URL를 조건으로 대상을 조회한다.
    rs = cs.execute(select_sql,(url_code,))
    result = rs.fetchall()
    print('  SELECT 쿼리 실행\n')

    print('  단어별 문자열 추출\n')
    for record in result:
        #print(record[0], record[1])

        string = record[0]

        # split() : Defalut는 공백으로 구분하여 문자열을 자른다. 특정문자 구분은 split("@") 괄호안에 특수문자 입력하여 사용
        string_split = string.split()

        #print(string_split)

        # LIST 형식으로 vals(파라메터)를 만들어 executemany 함수 사용
        # 중첩 for 문을 사용하여 건별(선별적) INSERT도 가능.
        vals = [(record[1], val) for val in string_split]
        cs.executemany("INSERT INTO REMAKE_DATA (DATA_LINK,DATA_TITLE_SPLIT) VALUES (:1,:2)", vals)


    delete_sql = "DELETE REMAKE_DATA WHERE DATA_TITLE_SPLIT IN ('...','추가추가')"
    cs.execute(delete_sql)
    print('  불필요 데이터 삭제 "...",.........\n')

    conn.commit()
    cs.close()
    conn.close()

if __name__ == '__main__':
    print('데이터 가공 작업 실행')
    db_remake()
    print('데이터 가공 작업 종료')