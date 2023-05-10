# -*- coding: utf-8 -*-
"""
Created on Mon May  8 23:33:47 2023

@author: shimi
"""
import re
import json
import pandas as pd
import glob


def get_column_names(schemas, ds_name, sorting_key='column_position'):
    column_details = schemas[ds_name]
    columns = sorted(column_details, key=lambda x: x[sorting_key])
    res = []
    for col in columns:
        res.append(col['column_name'])
    # print(res)
    return res


schemas = json.load(open('./schemas.json'))

order_columns = get_column_names(schemas, 'orders')

orders = pd.read_csv('./orders/part-00000', names=order_columns)

# print(orders)


def generate_json_filepath(src):
    root_path = 'retail_db_json'
    ds_path = re.split('[/\\\]', src)[0]
    file_path = re.split('[/\\\]', src)[1]
    tgt_file_path = f'{root_path}/{ds_path}/{file_path}'
    print(tgt_file_path)


src_file_names = glob.glob('*/part-*')
print(src_file_names)

for src in src_file_names:
    generate_json_filepath(src)
