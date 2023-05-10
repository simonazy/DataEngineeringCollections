# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import glob
import os
import pandas as pd
import json
import re


"""
Part one: use glob package to get file names
"""
# help(glob)
# help(glob.glob)
# print(os.getcwd())
# print(glob.glob('*/part-*'))
# print(glob.glob('*/retail_db/*/part-*'))


def get_column_name(schemas, ds_name, sorting_key='column_position'):
    column_details = schemas[ds_name]
    columns = sorted(column_details, key=lambda x: x[sorting_key])
    res = []
    for col in columns:
        res.append(col['column_name'])
    return res


def read_to_csv(src, schemas):
    ds_name = re.split('[/\\\]', src)[0]
    col_name = get_column_name(schemas, ds_name)
    df = pd.read_csv(src, names=col_name)
    return df


def csv_to_json(src, df):
    root_path = 'retail_db_json'
    ds_path = re.split('[/\\\]', src)[0]
    file_path = re.split('[/\\\]', src)[1]
    tgt_file_path = f'{root_path}/{ds_path}/{file_path}'
    os.makedirs(root_path, exist_ok=True)
    os.chmod('retail_db_json', 0o777)
    os.makedirs(f'{root_path}/{ds_path}/', exist_ok=True)
    os.chmod(f'{root_path}/{ds_path}/', mode=0o777)
    os.makedirs(tgt_file_path, mode=0o777, exist_ok=True)

    df.to_json(
        tgt_file_path,
        orient='records',
        lines=True)


def process_files():
    schemas = json.load(open('./schemas.json'))
    src_files = glob.glob('*/part-*')

    for src in src_files:
        print(f'Processing {src}')
        data = read_to_csv(src, schemas)
        csv_to_json(src, data)


process_files()
