import sys
sys.path.append('../')

import re, time
import requests
from bs4 import BeautifulSoup

from db.db_conn import *

# DB
config_file_path = './db/config.ini'
pc_option = 'db_name'
select_sql_query = 'select * from db_name.table_name'

# output
query_sql = "INSERT INTO table_name (user_id, news_index, comment) value ('{u}', '{i}', '{c}')"

# connect to DB
host_ip, user_id, user_pw, db_name = load_db_info_from_config(config_file_path, pc_option)  # get db information
cursor, mydb = connect_to_DB(host_ip, user_id, user_pw, db_name)

table_df_tmp = get_relation_df_w_columns(cursor, select_sql_query)
table_df = table_df_tmp.iloc[:, :]

print("DB Load")

try:
    for idx, row in table_df.iterrows():
        print(idx)
        news_index = row['news_index']
        url = row['url']

        headers = {"user-agent": "",
                    "referer" : '{}'.format(url)}

        oid=url.split("oid=")[1].split("&")[0]
        aid=url.split("aid=")[1]
        page = 1

        while True:
            c_url = "https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&templateId=default_society&pool=cbox5&_callback=jQuery1707138182064460843_1523512042464&lang=ko&country=&objectId=news" + oid + "%2C" + aid + "&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page=" + str(page) + "&refresh=false&sort=FAVORITE"
            r = requests.get(c_url, headers=headers)
            html = BeautifulSoup(r.content, "html.parser")
            # print(str(html).split('delCommentByUser":')[1].split(",")[0])
            # print(str(html).split('delCommentByMon":')[1].split(",")[0])
            time.sleep(2)

            # total_comm = int(str(html).split('comment":')[1].split(",")[0]) - (int(str(html).split('delCommentByUser":')[1].split(",")[0])+int(str(html).split('delCommentByMon":')[1].split(",")[0]))
            total_comm = str(html).split('comment":')[1].split(",")[0]

            name = re.findall('"userIdNo":([^\*]*),"exposedUserIp"', str(html)) #userIdNo
            if len(name) == 0:
                break
    
            # cont = re.findall('"contents":([.]*),"userIdNo"', str(html)) # 댓글
            cont = []
            for conidx in range(1, len(str(html).split('contents":'))):
                cont.append(str(html).split('contents":')[conidx].split('","')[0])

            for ix in range(len(name)):
                input_query_sql = query_sql.format(u=name[ix].replace('"',''), i=news_index, c=cont[ix].replace('\\','').replace('\'','‘'))
                cursor.execute(input_query_sql)

            if int(total_comm) <= ((page) * 20): #댓글 페이지 수 끝까지
                break
            else:
                page += 1
        
        if idx % 20 == 0:
            mydb.commit()
            print("index : ", idx, "news_index : ", news_index)
            print("댓글 총 개수 : ", total_comm, "", "commit 완료.")
            print()

    mydb.commit()

except Exception as e:
    print("index : ", idx, "news_index : ", news_index)
    print("댓글 총 개수 : ", total_comm)
    print("현재 댓글 페이지 : ", page)
    print("user 번호 : ", name[ix].replace('"',''))
    print(html)
    print(name, len(name))
    print(cont, len(cont))
    print(e)


## 댓글 크롤링 참고 출처 : https://blog.naver.com/PostView.naver?blogId=ky_s1919&logNo=222221259483&parentCategoryNo=&categoryNo=12&viewDate=&isShowPopularPosts=true&from=search