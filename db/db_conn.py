def load_db_info_from_config(config_file_path, pc_option):
  import configparser
  config = configparser.ConfigParser()
  config.read(config_file_path)
  pc_option = pc_option
  host_ip = config[pc_option]['host_ip']
  user_id = config[pc_option]['user_id']
  user_pw = config[pc_option]['user_pw']
  db_name = config[pc_option]['db_name']
  return host_ip, user_id, user_pw, db_name

def connect_to_DB(host_ip, user_id, user_pw, db_name):
  import pymysql
  # mydb = pymysql.connect(host=host_ip,
  #            user=user_id,
  #            passwd=user_pw,
  #            db=db_name,
  #            port=port_num)
  mydb = pymysql.connect(host=host_ip,
              user=user_id,
              passwd=user_pw,
              db=db_name)
              # port=port_num)
  cursor = mydb.cursor()
  return cursor, mydb


def get_relation_df(cursor, sql_query, column_list):
  import pandas as pd
  cursor.execute(sql_query)
  relation_tuple = cursor.fetchall()
  relation_df = pd.DataFrame(relation_tuple, columns=column_list)
  return relation_df


def get_relation_df_w_columns(cursor, sql_query):
  import pandas as pd
  cursor.execute(sql_query)
  field_names = [i[0] for i in cursor.description]
  relation_tuple = cursor.fetchall()
  relation_df = pd.DataFrame(relation_tuple, columns=field_names)
  return relation_df

# def input_dataframe_to_sql(host_ip, user_id, user_pw, db_name, df):
#     from sqlalchemy import create_engine
#     db_connection_str = 'mysql+pymysql://{db유저이름}:{db_password}@{host_address}/{db_name}'.format(user_id, user_pw, host_ip, db_name)