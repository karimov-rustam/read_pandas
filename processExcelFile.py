#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    print(df.head(10))
