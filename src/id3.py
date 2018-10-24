"""
 Create by xin.liu on : 2018/9/20 15:46
"""
# coding:utf-8
__author__ = 'xin.liu'


class Node(object):
    def __init__(self, attr_init=None, label_init=None, attr_down_init={}):
        # 当前节点的属性
        self.attr = attr_init
        # 节点的类标签
        self.label = label_init
        # 向下划分的属性取值
        self.attr_down = attr_down_init




