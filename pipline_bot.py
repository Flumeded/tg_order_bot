#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
from sqlalchemy import create_engine 
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Integer, String, Text, Date
import sqlalchemy as sa
from sqlalchemy.sql import select

db_config = {'user' : 'user1', # имя пользователя
             'pwd': '1111', # пароль
             'host': 'localhost', # адрес сервера
             'port': 5432,  # порт подключения
             'db': 'orders' } # название базы данных

#строка соединения с БД
connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_config['user'], 
	db_config['pwd'],
	db_config['host'],
	db_config['port'],
	db_config['db'])

# подключаемся к БД

engine  = create_engine(connection_string)
metadata = MetaData(engine)
conn = engine.connect()
metadata.reflect(bind = engine)
orders_list = metadata.tables['orders_list']


# выгрузка таблицы в пандас
order_for_table = '''SELECT * FROM  orders_list'''

raw = pd.io.sql.read_sql(order_for_table, con = engine, index_col = 'table_key')


#print(dict_insert)
def insert_order(dict_insert1):
    uniqu_number =  ''' SELECT MAX(uniq_number) FROM orders_list'''

    last_unique_number = pd.io.sql.read_sql(uniqu_number, con = engine).max()    

    ins = orders_list.insert().values(uniq_number= int(last_unique_number) + 1 , customer_name= dict_insert1['customer_name'], customer_unique_number= dict_insert1['customer_unique_number'], quantity= dict_insert1['quantity'], priority= dict_insert1['priority'], status = 0, order_time = sa.func.now(), link = dict_insert1['link'])
    conn.execute(ins)
    raw = pd.io.sql.read_sql(order_for_table, con = engine, index_col = 'table_key')


#query_insert = ''' INSERT INTO orders_list (uniq_number, customer_name, customer_unique_number, quantity, priority, status, order_time) VALUES ({}, {}, {}, {}, {}, {}, {}::timestamp) '''.format(1, "norma", "norma_number", 40, "Low", 0, "01/01/2020")

#engine.execute(query_insert)

def order_check_func(customer_unique_number, unique_number = 'all', data = raw):
    order_for_table = '''SELECT * FROM  orders_list'''
    data = pd.io.sql.read_sql(order_for_table, con = engine, index_col = 'table_key')
    data = data.loc[data.loc[:, 'customer_unique_number'] == customer_unique_number]
    data['st'] = data['status'].apply(lambda x: 'ready' if x == 1 else 'not ready')
    if unique_number == 'all':
        x = ''
        for i in data['uniq_number'].to_list():
            data1 = data[data['uniq_number'] == i]
            j = "Unique nuber: {}, Quantity: {}, Link: {}, Status: {}".format(str(i), data1['quantity'].values, data1['link'].values, data1['st'].values)
            x = x +"\n  {}".format(j)
        return x
    elif unique_number == 'last':
        x = ''
        data1 = data[data['uniq_number'] == data['uniq_number'].max()]
        j = "Unique nuber: {}, Quantity: {}, Link: {}, Status: {}".format(data1['uniq_number'].values, data1['quantity'].values, data1['link'].values, data1['st'].values)
        x = x +"\n  {}".format(j)
        return x
    else:
        
        if int(unique_number) in data['uniq_number'].to_list():
            data1 = data[data['uniq_number'] == unique_number]
            j = "Unique nuber: {}, Quantity: {}, Link: {}, Status: {}".format(data1['uniq_number'].values, data1['quantity'].values, data1['link'].values, data1['st'].values)
            
            return str(j)
        else:
            x = 'Are you gay? Number is not correct!'
            return x 



def order_delete(customer_unique_number, uniq_number):
    order_for_table = '''SELECT * FROM  orders_list'''
    data = pd.io.sql.read_sql(order_for_table, con=engine, index_col='table_key')
    data = data.loc[data.loc[:, 'customer_unique_number'] == customer_unique_number]
    if int(uniq_number) in data['uniq_number'].to_list():
        delete_query = '''DELETE FROM orders_list WHERE uniq_number = {}'''.format(uniq_number)
        engine.execute(delete_query)
        return('Заказ №{} успешно удален'.format(uniq_number)),


    else:
        return('Are you gay? Number is not correct!')


def order_statu_update(uniq_number):
    update_status_query = '''UPDATE orders_list SET status = 1 WHERE  uniq_number = {}'''.format(int(uniq_number))
    engine.execute(update_status_query)
    order_for_table = '''SELECT * FROM  orders_list'''
    data = pd.io.sql.read_sql(order_for_table, con=engine, index_col='table_key')
    j = data.loc[data.loc[:, 'uniq_number'] == uniq_number]
    return int(j['customer_unique_number'].values)



print('pipeline conected')

#query = ''' SELECT * FROM orders_list '''

#data_raw = pd.io.sql.read_sql(query, con = engine, index_col = 'table_key')

#print(raw)
#print(' ')
#print(int(last_unique_number))
