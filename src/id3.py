"""
 Create by xin.liu on : 2018/9/20 15:46
"""
# coding:utf-8
__author__ = 'xin.liu'

from math import log2


class Node(object):
    def __init__(self, attr=None, label=None, attr_down={}):
        # 当前节点的属性
        self.attr = attr
        # 节点的类标签
        self.label = label
        # 向下划分的属性取值
        self.attr_down = attr_down


def NodeLabel(label_arr):
    label_count = {}
    for label in label_arr:
        if label in label_count:
            label_count[label] += 1
        else:
            label_count[label] = 1
    return label_count

def InfoEnt(label_arr):
    ent = 0
    n = len(label_arr)
    label_count = NodeLabel(label_arr)
    for label in label_count:
        ent -= (label_count[label] / n ) * log2(label_count[label] / n)
    return ent


def InfoGain(df, idx):
    info_gain = InfoEnt(df.iloc[:,-1])
    div_value = 0
    n = len(df[idx])
    if df[idx].dtypes == (float, int):
        sub_info_ent = {}
        df = df.sort_values(by=idx, ascending=1)
        df = df.reset_index(drop=True)
        data_arr = df[idx]
        label_arr = df.iloc[:,-1]
        for i in range(n-1):
            div = (data_arr[i] + data_arr[i+1]) / 2
            sub_info_ent[div] = ((i + 1) * InfoEnt(label_arr[0:i+1]) / n) \
                                + ((n - i - 1) * InfoEnt(label_arr[i+1:-1]) / n)
        div_value, sub_info_ent_max = min(sub_info_ent.items(), key=lambda x: x[1])
        info_gain -= sub_info_ent_max
    else:
        data_arr = df[idx]
        label_arr = df.iloc[:,-1]
        value_count = NodeLabel(data_arr)
        for attr in value_count:
            key_label_arr = label_arr[data_arr == attr]
            info_gain -= value_count[attr] * InfoEnt(key_label_arr) / n
    return info_gain, div_value


def OptAttr(df):
    info_gain = 0
    opt_attr = 0
    div_value = 0
    for idx in df.columns[0:-1]:
        info_gain_temp, div_value_temp = InfoGain(df, idx)
        if info_gain_temp > info_gain:
            info_gain = info_gain_temp
            opt_attr = idx
            div_value = div_value_temp
    return opt_attr, div_value


def TreeGenerate(df):
    new_node = Node(attr=None, label=None, attr_down={})
    label_arr = df.iloc[:, -1]
    label_count = NodeLabel(label_arr)
    if label_count:
        new_node.label = max(label_count, key=label_count.get)
        if len(label_count) == 1 or len(label_count) == 0:
            return new_node
        new_node.attr, div_value = OptAttr(df)
        if div_value == 0:
            value_count = NodeLabel(df[new_node.attr])
            for key in value_count:
                df_set = df[df[new_node.attr] == key]
                df_set = df_set.drop(new_node.attr, 1)
                new_node.attr_down[key] = TreeGenerate(df_set)
        else:
            value_l = "<=%.3f" % div_value
            value_r = "<=%.3f" % div_value
            df_l = df[df[new_node.attr] <= div_value]
            df_r = df[df[new_node.attr] > div_value]
            new_node.attr_down[value_l] = TreeGenerate(df_l)
            new_node.attr_down[value_r] = TreeGenerate(df_r)
    return new_node





