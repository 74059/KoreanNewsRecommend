import sys
sys.path.append('../')

import time
import requests
from bs4 import BeautifulSoup
from datetime import timedelta, date, datetime

from db.db_conn import *

# dataframe
# [뉴스index] [제목] [언론사] [URL]
# [title] [company] [url]

# DB
config_file_path = './db/config.ini'
pc_option = 'db_name'

# output
query_sql = "INSERT INTO table_name (title, company, url) value ('{t}', '{c}', '{u}')"

# connect to DB
host_ip, user_id, user_pw, db_name = load_db_info_from_config(config_file_path, pc_option)  # get db information
cursor, mydb = connect_to_DB(host_ip, user_id, user_pw, db_name)

print("Load")

## main
headers = {"user-agent": ""}

sections = {
    # "정치" : '100',
    # "경제" : '101',
    # "사회" : '102',
    # "생활/문화" : '103',
    # "세계" : '104',
    "IT/과학" : '105'
}

two = ['type06_headline', 'type06']

try:
    for section in sections: # section For문
        for n in range(72): # 날짜 For문 # 96
            c_date = date(2022, 1, 26) + timedelta(days = n)
            da = datetime.strftime(c_date, '%Y-%m-%d').replace('-', '')
            for page in range(1, 151): # page 150까지 가져오기
                news_site_url = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1={section}&date={d}&page={p}'

                r = requests.get(news_site_url.format(section=sections[section], d=da, p=page), headers=headers)
                soup = BeautifulSoup(r.text, 'html.parser')

                for one in two: # 기사 파트가 headline과 아닌 것 두 파트로 나누어있어서, 그거에 대한 For문
                    sources = soup.select('div.list_body.newsflash_body > ul.{} > li dl dt > a'.format(one))[1::2] # 홀수번째 list값 추출. 같은 값이 두 번 나옴.
                    sources_news_site = soup.select('div.list_body.newsflash_body > ul.{} > li dl dd > span.writing'.format(one))

                    for i in range(len(sources)):
                        # news_title = sources[i].text.strip()
                        # if len(news_title) == 0 :
                            # continue
                        news_title = sources[i].text.strip().replace('\'', '‘')
                        news_url = sources[i].attrs['href']
                        news_company = sources_news_site[i].text.strip()

                        input_query_sql = query_sql.format(t=news_title, c=news_company, u=news_url)
                        cursor.execute(input_query_sql)

                        if i % 10 == 0:
                            mydb.commit()
            if page % 10 == 0:
                time.sleep(2)

    mydb.commit()
except Exception as e:
    print("쿼리문 : ", input_query_sql)
    print("섹션 : ", section)
    print("날짜 : ", c_date)
    print("페이지 : ", page)
    print(e)