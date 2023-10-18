import sys
sys.path.append('../')

import re
import numpy as np
from gensim.models import Word2Vec

from db.db_conn import *

# DB
config_file_path = './db/config.ini'
pc_option = 'db_name'
select_sql_query = 'select * from db_name.wikidata'

# output
save_path = './myprj/our_data' + '/'
save_fname = 'entity_embedding_ours.vec'

# connect to DB
host_ip, user_id, user_pw, db_name = load_db_info_from_config(config_file_path, pc_option)  # get db information
cursor, mydb = connect_to_DB(host_ip, user_id, user_pw, db_name)

table_df_tmp = get_relation_df_w_columns(cursor, select_sql_query)
table_df = table_df_tmp.iloc[:, :]
table_df.sort_values(by=['id'], axis=0)

print("DB Load")

wikiword_list = list(np.array(table_df['word'].tolist()))

X_train = []
for idx, row in table_df.iterrows():
    exp_khaiii = row['exp_khaiii']
    
    exp_khaiii_rm = re.sub('[^A-Za-z0-9가-힣+]', ' ', str(exp_khaiii))
    exp_khaiii_list = exp_khaiii_rm.split()
    X_train.append(exp_khaiii_list)
print("X_train 길이 : ", len(X_train))

model = Word2Vec(sentences = X_train, vector_size = 100, window = 3, min_count=3, workers = 3, sg = 1) # min_count=3
model.save(save_path + 'word2vec_80000.model')
print("min_count 3일 때 '코로나'와 관련있는 단어 : ", model.wv.most_similar('코로나'))

f = open(save_path + save_fname, 'w')
error_word_list = []
for idx, row in table_df.iterrows():
    try:
        wikiid = row['id']
        wikiword = row['word']

        # print(wikiword)
        model.wv[wikiword]

        write_vec = wikiid
        for num in model.wv[wikiword]:
            write_vec += '\t' + str(num)
        write_vec += '\n'
        f.write(write_vec)

    except KeyError as e:
        error_word_list.append(wikiword)
        continue
    except Exception as e:
        print(e)
        # pass
f.close()
ef = open(save_path + 'except_error_word_list', 'w')
ef.write(str(error_word_list))
ef.close()