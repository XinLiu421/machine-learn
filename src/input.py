"""
 Create by xin.liu on : 2018/9/20 15:46
"""
# coding:utf-8
__author__ = 'xin.liu'

import pandas as pd
from src.id3 import tree_generate


def prepare_data():
    id3_data = pd.read_csv("../data/decision_tree.csv")
    return id3_data


if __name__ == '__main__':
    id3_data = prepare_data()
    decision_tree = tree_generate(id3_data)
    print(decision_tree)
