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


def node_label(label_arr):
    label_count = {}
    for label in label_arr:
        if label in label_count:
            label_count[label] += 1
        else:
            label_count[label] = 1
    return label_count


def info_ent(label_arr):
    try:
        from math import log2
    except ImportError:
        print("module math.log2 not found")

    ent = 0
    n = len(label_arr)
    label_count = node_label(label_arr)

    for key in label_count:
        ent -= (label_count[key] / n) * log2(label_count[key] / n)
    return ent


def value_count(data_arr):
    value_counts = {}
    for label in data_arr:
        if label in value_counts:
            value_counts[label] += 1
        else:
            value_counts[label] = 1
    return value_counts


def cal_info_gain(df, index):
    info_gain = info_ent(df.values[:, -1])
    div_value = 0

    n = len(df[index])

    # 1 处理 连续变量
    if df[index].dtypes == (float, int):
        sub_info_ent = {}
        df = df.sort_values(by=index, ascending=1)
        df = df.reset_index(drop=True)

        data_arr = df[index]
        label_arr = df[df.columns[-1]]

        for i in range(n-1):
            div = (data_arr[i] + data_arr[i+1]) / 2
            sub_info_ent[div] = ((i+1) * info_ent(label_arr[0:i+1]) / n) \
                                + ((n-i-1) * info_ent(label_arr[i+1:-1]) / n)
        div_value, sub_info_ent_max = min(sub_info_ent.items(), key=lambda x: x[1])
        info_gain -= sub_info_ent_max

    # 2 处理 分类变量
    else:
        data_arr = df[index]
        label_arr = df[df.columns[-1]]
        value_counts = value_count(data_arr)
        for key in value_counts:
            key_label_arr = label_arr[data_arr == key]
            info_gain -= value_counts[key] * info_ent(key_label_arr) / n
    return info_gain, div_value


def get_opt_attr(df):
    info_gain = 0

    for attr_id in df.columns[0:-1]:
        info_gain_tmp, div_value_tmp = cal_info_gain(df, attr_id)
        if info_gain_tmp > info_gain:
            info_gain = info_gain_tmp
            opt_attr = attr_id
            div_value = div_value_tmp
    return opt_attr, div_value


def tree_generate(df):
    new_node = Node(None, None, {})
    label_arr = df[df.columns[-1]]
    label_count = node_label(label_arr)

    if label_count:
        new_node.label = max(label_count, key=label_count.get)

        if len(label_count) == 1 or len(label_count) == 0:
            return new_node

        new_node.attr, div_value = get_opt_attr(df)

        if div_value == 0:
            value_counts = value_count(df[new_node.attr])
            for value in value_counts:
                df_v = df[df[new_node.attr].isin([value])]


