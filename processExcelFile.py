#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
import pandas as pd
import argparse


def processExcelFile(name, course, skipRow=12, cols=[0, 2, 5]):
    xl = pd.ExcelFile(name)
    df = xl.parse(skiprows=skipRow)

    # noinspection PyTypeChecker
    df.drop(df.columns[cols], axis=1, inplace=True)
    df.dropna(inplace=True)
    df.columns = ['item', 'count', 'price']
    df.reset_index(drop=True, inplace=True)
    df['price'] /= course

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Excel file')
    parser.add_argument('name', help='Name of Excel file to process')
    parser.add_argument('course',
                        help='Currency course. Default value is 69.75',
                        nargs='?',
                        default=69.75,
                        type=float)
    args = parser.parse_args()
    df = processExcelFile(args.name, args.course)

    engine = create_engine('postgres://lxuser@localhost:5432/test_db')
    database = pd.io.sql.SQLDatabase(engine)

    if not database.has_table('items'):
        args = ['items', database]
        kwargs = {
            'frame': df,
            'index': True,
            'index_label': 'id',
            'keys': 'id'
        }
        table = pd.io.sql.SQLTable(*args, **kwargs)
        table.create()

    df.to_sql('items', con=engine, if_exists='append', index=False)
