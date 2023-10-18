# comment 크롤링한 뉴스 개수 : 69300, N162368
import sys
sys.path.append('../')

from db.db_conn import *

# DB
config_file_path = './db/config.ini'
pc_option = 'db_name'
select_sql_query = 'select * from db_name.user_history'

# output
query_sql = "INSERT INTO user_history_dup (user_id, news_index) value ('{u}', '{n}')"

# connect to DB
host_ip, user_id, user_pw, db_name = load_db_info_from_config(config_file_path, pc_option)  # get db information
cursor, mydb = connect_to_DB(host_ip, user_id, user_pw, db_name)

table_df_tmp = get_relation_df_w_columns(cursor, select_sql_query)
table_df = table_df_tmp.iloc[:, :]

# duplicate
table_df_dup = table_df.drop_duplicates(['user_id', 'news_index'],keep='first').reset_index()
print('기존 데이터 개수 : ', len(table_df))
print('dup 한 후 : ',len(table_df_dup))
print(table_df_dup.head(5))

# commit
for idx, row in table_df_dup.iterrows():
    user_id = row['user_id']
    news_index = row['news_index']

    input_query_sql = query_sql.format(u=user_id, n=news_index)
    cursor.execute(input_query_sql)

mydb.commit()