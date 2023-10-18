import sys
sys.path.append('../')

import re
from khaiii import KhaiiiApi

from db.db_conn import *

# DB
config_file_path = './db/config.ini'
pc_option = 'db_name'
select_sql_query = 'select * from db_name.news_model_past'

# output
query_sql = 'UPDATE news_model_past SET word="{w}" WHERE news_index="{i}"'

# connect to DB
host_ip, user_id, user_pw, db_name = load_db_info_from_config(config_file_path, pc_option)  # get db information
cursor, mydb = connect_to_DB(host_ip, user_id, user_pw, db_name)

table_df_tmp = get_relation_df_w_columns(cursor, select_sql_query)
df = table_df_tmp.iloc[:, :] # 다시 시작할 곳 작성

print("Load Done")

# for preprocessing
significant_pos_list = ['NNG', 'NNP']
stopwords = ['헤럴드', '데일리안', '뉴스', '오늘', '영상', '오늘뉴스']

try:
    for idx, row in df.iterrows():
        news_index = row['news_index']    
        title = row['title']  # POS Tagging할 값  

        # remove special characters
        sc_removed_rt = re.sub('[^A-Za-z0-9가-힣+]', ' ', title)   
        sc_removed_rt = ' '.join(sc_removed_rt.split())

        if len(sc_removed_rt) < 5:
            continue

        # for POS tagging    
        kapi = KhaiiiApi()  

        title_sent = kapi.analyze(sc_removed_rt)
        
        significant_word_list = []
        for word in title_sent:
            word = str(word)
            word_str = word.split('\t')[1]
            word_list = re.split(' \+ |\. | ', word_str)
            for emt in word_list:
                word_emt = emt.split('/')
                if word_emt[1] in significant_pos_list:
                    if word_emt[0] not in stopwords:
                        significant_word_list.append(word_emt[0])
        significant_word_list_dup = list(set(significant_word_list))

        # mysql
        input_query_sql = query_sql.format(w=significant_word_list_dup, i=news_index)
        cursor.execute(input_query_sql)

        # print log
        if idx % 100000 == 0:
            mydb.commit()
            print(idx,"/",len(table_df_tmp))
            print('title : ', title)  
            print('word : ', significant_word_list_dup)        
            print()

    mydb.commit()
except Exception as e:
    print(idx,"/",len(table_df_tmp))
    print('news_index : ', news_index)
    print('title : ', title) 
    print('sc_removed_rt : ', sc_removed_rt) 
    print('word : ', significant_word_list_dup)    
    print(input_query_sql)    
    print(e)