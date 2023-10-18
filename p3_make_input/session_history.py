import sys
sys.path.append('../')

import random
import re, pickle
import pandas as pd

from db.db_conn import *
from module.entity_embedding_module import *

# DB
config_file_path = './db/config.ini'
pc_option = 'db_name'
select_sql_query = 'select * from db_name.user_history_dup'
past_sql_query = 'select * from db_name.news_model_past'

# output
save_path = './myprj/our_data' + '/'
save_fname = 'session_list.pkl'
save_h_fname = 'history_dict.pkl'

# connect to DB
host_ip, user_id, user_pw, db_name = load_db_info_from_config(config_file_path, pc_option)  # get db information
cursor, mydb = connect_to_DB(host_ip, user_id, user_pw, db_name)

table_df_tmp = get_relation_df_w_columns(cursor, select_sql_query)
table_df = table_df_tmp.iloc[:, :] # 얘네 뉴스개수 14438

news_model_past_df_tmp = get_relation_df_w_columns(cursor, past_sql_query)
news_model_past_df = news_model_past_df_tmp.iloc[:500000, :]

print("DB Load")

table_groupby = table_df.groupby('user_id')['news_index'].apply(lambda x: "[%s]" % ', '.join(x))
table_groupby_df = table_groupby.reset_index(drop=False)

all_news_index = list(set(list(news_model_past_df['news_index'])))

rdlist_3 = [1, 2, 3]
rdlist_1 = [0, 1]
rdlist_7 = [7, 8, 9, 10, 11, 12, 13, 14, 15]
all_session_list = []
all_history_dict = {}
for idx, row in table_groupby_df.iterrows():
    user_session_list = []
    user_id = row['user_id']
    news_index = row['news_index']

    news_index_rm = re.sub('[^A-Za-z0-9가-힣+]', ' ', str(news_index))
    news_index_list = news_index_rm.split()

    ## history
    all_history_dict[user_id] = news_index_list

    ## session
    # 1. user
    user_session_list.append(user_id)

    # 2. user_history(uh)
    # 3. user에게 노출된 뉴스 중 1번 이상 클릭한 기사들(oneclick_list)
    if len(news_index_list) > 25:
        oneclick_list = random.sample(news_index_list, 6)
    elif len(news_index_list) > 10:
        rdnum = int(random.sample(rdlist_3, 1)[0])
        oneclick_list = random.sample(news_index_list, rdnum)
    elif len(news_index_list) > 3:
        rdnum = int(random.sample(rdlist_1, 1)[0])
        oneclick_list = random.sample(news_index_list, rdnum)
    else:
        oneclick_list = []

    uh = [x for x in news_index_list if x not in oneclick_list]

    user_session_list.append(uh)
    user_session_list.append(oneclick_list)

    rm = []
    # 4. user에게 노출되었으나, 클릭하지 않는 기사들(noclick_list)
    rdnum = int(random.sample(rdlist_7, 1)[0])
    noclick_list = random.sample(all_news_index, rdnum)
    for noclick_elt in noclick_list:
        if noclick_elt in news_index_list:
            rm.append(noclick_elt)
    noclick_list = [x for x in noclick_list if x not in rm]
    user_session_list.append(noclick_list)

    # 전체에 append
    all_session_list.append(user_session_list)


with open(save_path + save_fname,'wb') as f: # 쓸 때 wb, 가져올 때 rb
    pickle.dump(all_session_list,f)

f.close()

with open(save_path + save_h_fname,'wb') as ff:
    pickle.dump(all_history_dict, ff)

ff.close()