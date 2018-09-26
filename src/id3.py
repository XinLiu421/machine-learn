"""
 Create by xin.liu on : 2018/9/20 15:46
"""
# coding:utf-8
__author__ = 'xin.liu'

import pandas as pd
from src.decision_tree import tree_generate


def prepare_data():
    data = pd.read_csv("../data/test.csv")
    return data


# def test_decision_tree():


if __name__ == '__main__':
    data = prepare_data()
    tree_generate(data)
