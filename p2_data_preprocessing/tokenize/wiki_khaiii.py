import sys
sys.path.append('../')

import re
from khaiii import KhaiiiApi

from db.db_conn import *

# DB
config_file_path = './db/config.ini'
pc_option = 'db_name'
select_sql_query = 'select * from db_name.wikidata'

# output
query_sql = 'UPDATE wikidata SET exp_khaiii="{e}" WHERE word="{w}"'

# connect to DB
host_ip, user_id, user_pw, db_name = load_db_info_from_config(config_file_path, pc_option)  # get db information
cursor, mydb = connect_to_DB(host_ip, user_id, user_pw, db_name)

table_df_tmp = get_relation_df_w_columns(cursor, select_sql_query)
table_df = table_df_tmp.iloc[:, :] # len(2558) 진행 완료

print("DB Load")

# for preprocessing
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

try:
    for idx, row in table_df.iterrows():
        word = row['word']
        exp = row['exp']
        exp_khaiii = row['exp_khaiii']

        if exp_khaiii != None:
            continue

        # remove special characters
        sc_removed_rt = re.sub('[^A-Za-z0-9가-힣+]', ' ', exp)   
        sc_removed_rt = ' '.join(sc_removed_rt.split())

        if len(sc_removed_rt) < 5:
            continue

        kapi = KhaiiiApi()
        title_sent = kapi.analyze(sc_removed_rt)

        significant_word_list = []
        for word_in_khaiii in title_sent:
            word_in_khaiii = str(word_in_khaiii)
            word_k_str = word_in_khaiii.split('\t')[1]
            word_k_list = re.split(' \+ |\. | ', word_k_str)
            for emt in word_k_list:
                word_emt = emt.split('/')
                if (word_emt[0] not in stopwords) and (len(word_emt[0]) >= 2):
                    significant_word_list.append(word_emt[0])
        significant_word_list_dup = list(set(significant_word_list))
        input_query_sql = query_sql.format(e = significant_word_list_dup, w = word)
        cursor.execute(input_query_sql)
    mydb.commit()
except Exception as e:
    print(idx,"/",len(table_df_tmp))
    print(input_query_sql)
    print("exp_khaiii : ", significant_word_list_dup, len(significant_word_list_dup))
    print(e)