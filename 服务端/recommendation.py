#-*- coding: UTF-8 -*-
"""
基于Apriori算法实现推荐功能.
训练关联规则模型（Apriori）以查找过去一段时间用户所听音乐类型
的最相关项.该算法将大多数用户的产品偏好关联起来，并可用于生成音乐类型
推荐.
"""

from __future__ import print_function, division
import pandas as pd
from apriori import apriori
import json
import collections

################################################################################
#基于Apriori算法实现推荐功能
################################################################################
def recommedation(path = './Music_Recommendation.csv', **kwargs):
    """
    基于Apriori算法实现推荐功能.
    按照lift得分排序，推荐得分最高的前n个组合,
    既打印结果,也以json形式返回结果.

    :param
        path --  文件路径(str),文件必须是csv文件.
    :keyword
        min_support -- 最小关系支持度值(support)(float).
        min_confidence -- 最小关系置信度值(confidence)(float).
        min_lift -- 最小关系提升度值(lift)(float).
        max_length -- 关系最大长度(int).
        num -- 推荐lift得分最高的前num个组合，即推荐个数(int).
    """
    # 解析参数
    min_support = kwargs.get('min_support', 0.1)
    min_confidence = kwargs.get('min_confidence', 0.0)
    min_lift = kwargs.get('min_lift', 0.0)
    max_length = kwargs.get('max_length', None)
    num = kwargs.get('num', 10)

    # 加载数据
    dataset = pd.read_csv(path, names = list(range(0, 20)))
    # 将每一条用户数据以列表的形式加入列表
    transactions = []
    for i in range(0, len(dataset)):
        vals = []
        for j in range(0, len(dataset.keys())):
            val = str(dataset.values[i,j])
            # 判断是否是空值,如果是空值,省略
            if val != 'nan':
                vals.append(val)
        transactions.append(vals)

    # 调用Apriori算法预测结果
    rules = apriori(transactions, min_support = min_support, min_confidence = min_confidence, min_lift = min_lift,
                    max_length = max_length)

    # 可视化结果
    results = list(rules)
    lift = []
    association = []
    for i in range (0, len(results)):
        lift.append(results[:len(results)][i][2][0][3])
        association.append(list(results[:len(results)][i][0]))
    rank = pd.DataFrame([association, lift]).T
    rank.columns = ['Association', 'Lift']
    # 按照lift得分排序，推荐得分最高的前n个组合
    results = rank.sort_values('Lift', ascending=False)
    # 满足条件的结果个数
    size = len(results)
    # 如果满足条件的结果个数小于要求的输出个数,
    # 则输出全部结果
    if size < num:
        num = size
    # 打印结果
    print(results.head(num))

    # 将结果以json格式返回
    # 有序字典
    results_json = collections.OrderedDict()
    for i in range(num):
        results_json[str(results.iloc[i, : ]['Association'])] = \
            results.iloc[i, :]['Lift']
    return json.dumps(results_json)

################################################################################
#函数入口
################################################################################
if __name__ == '__main__':
    # 文件路径(str),文件必须是csv文件
    # 默认路径
    # path = './Music_Recommendation.csv'
    # 随机生成文件路径
    path = './Music_Recommendation_Random.csv'

    # 基于Apriori算法实现推荐功能.
    results_json = recommedation(path, min_support = 0.003, min_confidence = 0.2, min_lift = 3, max_length = 5, num = 10)
    print(results_json)