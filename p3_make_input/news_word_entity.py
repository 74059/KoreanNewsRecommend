import sys
sys.path.append('../')

import re, pickle

from db.db_conn import *

# DB
config_file_path = './db/config.ini'
pc_option = 'db_name'
select_sql_query = 'select * from db_name.wikidata'
past_sql_query = 'select * from db_name.news_model_past'

# output
save_path = './myprj/our_data' + '/'
save_fname = 'news_words_dict.pkl'
save_h_fname = 'news_entities_dict.pkl'

# connect to DB
host_ip, user_id, user_pw, db_name = load_db_info_from_config(config_file_path, pc_option)  # get db information
cursor, mydb = connect_to_DB(host_ip, user_id, user_pw, db_name)

table_df_tmp = get_relation_df_w_columns(cursor, select_sql_query)
table_df = table_df_tmp.iloc[:, :] # 여기 뉴스개수 14438

entity_dict = table_df[['id', 'word']].set_index('word').T.to_dict() # id 가 value, word가 key

news_model_past_df_tmp = get_relation_df_w_columns(cursor, past_sql_query)
news_model_past_df = news_model_past_df_tmp.iloc[:500000, :]

print("DB Load")

all_news_words = {}
all_news_entities = {}
no_in_wikipedia = []
for idx, row in news_model_past_df.iterrows():
    news_index = row['news_index']
    word = row['word']
    entity = row['entity']

    word_rm = re.sub('[^A-Za-z0-9가-힣+]', ' ', str(word))
    word_list = word_rm.split()

    entity_rm = re.sub('[^A-Za-z0-9가-힣+]', ' ', str(entity))
    entity_list = entity_rm.split()

    ## news_words
    all_news_words[news_index] = word_list

    ## news_entities
    entities_list = []
    for e in entity_list:
        one_entity = []
        one_entity.append(e)

        if e not in entity_dict:
            continue
        entity_id = entity_dict[e]['id']
        tup = (one_entity, entity_id)

        entities_list.append(tup)

    all_news_entities[news_index] = entities_list


with open(save_path + save_fname,'wb') as f: # 쓸 때 wb, 가져올 때 rb
    pickle.dump(all_news_words,f)

f.close()

with open(save_path + save_h_fname,'wb') as ff:
    pickle.dump(all_news_entities, ff)

ff.close()

no_in_wikipedia = list(set(no_in_wikipedia))
with open(save_path + 'no_in_wikipedia','wb') as f:
    pickle.dump(all_news_entities, f)