import sys
sys.path.append('../')

from db.db_conn import *

# DB
config_file_path = './db/config.ini'
pc_option = 'db_name'
select_sql_query = 'select * from db_name.news_model_p'

# output
query_sql = "INSERT INTO news_model_past (news_index, title, company, url) value ('{i}', '{t}', '{c}', '{u}')"

# connect to DB
host_ip, user_id, user_pw, db_name = load_db_info_from_config(config_file_path, pc_option)  # get db information
cursor, mydb = connect_to_DB(host_ip, user_id, user_pw, db_name)

table_df_tmp = get_relation_df_w_columns(cursor, select_sql_query)
table_df = table_df_tmp.iloc[:, :]

print("Load")

# 제목 중복값 제거
table_df_dup = table_df.drop_duplicates(['title'],keep='first').reset_index()
print('기존 데이터 개수 : ', len(table_df))
print('dup 한 후 : ',len(table_df_dup))

# db insert
try:
    for idx, row in table_df_dup.iterrows():
        title = row['title']
        company = row['company']
        url = row['url']

        if len(title) == 0 :
            continue
        elif title == '동영상기사':
            continue

        if len(company) == 0 :
            continue
        
        if len(url) == 0 :
            continue
        
        news_idx = 'N' + str(idx)

        input_query_sql = query_sql.format(i=news_idx, t=title, c=company, u=url)
        cursor.execute(input_query_sql)

        if idx % 10000 == 0:
            mydb.commit()

    mydb.commit()

except Exception as e:
    mydb.commit()
    print("index : ", idx, ", news_index : ", news_idx)
    print("title : ", title)
    print("company : ", company)
    print("url : ", url)
    print("error message : ", e)