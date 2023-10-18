import sys
sys.path.append('../')

import re, time
import numpy as np
import wikipediaapi

from db.db_conn import *

# DB
config_file_path = './db/config.ini'
pc_option = 'db_name'
select_sql_query = 'select * from db_name.news_model_past'
select_sql_query_wikidata = 'select * from db_name.wikidata'

# output
query_sql = 'INSERT INTO wikidata (id, word, exp) value ("{i}", "{w}", "{e}")'

# connect to DB
host_ip, user_id, user_pw, db_name = load_db_info_from_config(config_file_path, pc_option)  # get db information
cursor, mydb = connect_to_DB(host_ip, user_id, user_pw, db_name)

table_df_tmp = get_relation_df_w_columns(cursor, select_sql_query)
wikidata_df = get_relation_df_w_columns(cursor, select_sql_query_wikidata)
table_df = table_df_tmp.iloc[300001:, :] # 일단 기사 20000개만으로 entity_embedding # 30만1 진행할 차례

print("DB Load")

wiki = wikipediaapi.Wikipedia('ko')

wikiword_list = list(np.array(wikidata_df['word'].tolist()))

try:
    word_id = len(wikiword_list)
    for idx, row in table_df.iterrows():
        word_str = row['word']
        word_str_rm = re.sub('[^A-Za-z0-9가-힣+]', ' ', str(word_str))
        word_list = list(set(' '.join(word_str_rm.split()).split()))

        for word_em in word_list:
            if word_em in wikiword_list:
                continue
            wikiword_list.append(word_em)
            wikipage = wiki.page(word_em)
            if wikipage.exists() == True:
                time.sleep(2)
                word = wikipage.title
                wiki_summary = re.sub('[^A-Za-z0-9가-힣+]', ' ', str(wikipage.summary))
                wiki_summary = ' '.join(wiki_summary.split())
                if len(wiki_summary) > 200:
                    entity = wiki_summary[0:200]
                else:
                    entity = wiki_summary
                input_query_sql = query_sql.format(i="Q" + str(word_id), w=word_em, e=entity)
                cursor.execute(input_query_sql)
                word_id += 1

        if idx % 10000 == 0:
            mydb.commit()
            print(idx,"/",len(table_df_tmp))
            print('word_list : ', word_list)     
            print()
    mydb.commit()
except Exception as e:
    mydb.commit()
    print(idx,"/",len(table_df_tmp))
    print('word_list : ', word_list)
    print(word_em, ":", wikipage.exists())
    print(e)