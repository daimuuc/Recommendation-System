#-*- coding: UTF-8 -*-
"""
实现Apriori算法.
直接调用apriori函数即可.
API Usage：
    transactions = [
        ['beer', 'nuts'],
        ['beer', 'cheese'],
    ]
    results = list(apriori(transactions))

关于Apriori算法的概念参考
博客https://westerly-lzh.github.io/cn/2015/08/DM001-Apriori/.

"""

from __future__ import print_function, division
from collections import namedtuple
from itertools import combinations

################################################################################
# 数据结构
################################################################################
class TransactionManager(object):
    """
    事务管理器.
    """

    def __init__(self, transactions):
        """
        初始化函数.

        :param
            transactions -- 一个可迭代事务对象
                            (eg. [['A', 'B'], ['B', 'C']]).
        """
        self.__num_transaction = 0
        self.__items = []
        self.__transaction_index_map = {}

        for transaction in transactions:
            self.add_transaction(transaction)

    def add_transaction(self, transaction):
        """
        增加一个事务

        :param
            transaction -- 作为可迭代对象的事务 (eg. ['A', 'B']).
        """
        for item in transaction:
            if item not in self.__transaction_index_map:
                self.__items.append(item)
                self.__transaction_index_map[item] = set()
            self.__transaction_index_map[item].add(self.__num_transaction)
        self.__num_transaction += 1

    def calc_support(self, items):
        """
        返回项的支持度(support).

        :param
            items -- 作为可迭代对象的项 (eg. ['A', 'B']).
        """
        # 空项是被所有事务支持的.
        if not items:
            return 1.0

        # 空事务不支持任何项.
        if not self.num_transaction:
            return 0.0

        # 创建事务索引交集.
        sum_indexes = None
        for item in items:
            indexes = self.__transaction_index_map.get(item)
            if indexes is None:
                # 不支持包含不存在的项目的任何集合.
                return 0.0

            if sum_indexes is None:
                # 第一次分配索引.
                sum_indexes = indexes
            else:
                # 计算交集
                sum_indexes = sum_indexes.intersection(indexes)

        # 计算并返回支持度.
        return float(len(sum_indexes)) / self.__num_transaction

    def initial_candidates(self):
        """
        返回初始候选项.
        """
        return [frozenset([item]) for item in self.items]

    @property
    def num_transaction(self):
        """
        返回事务的个数.
        """
        return self.__num_transaction

    @property
    def items(self):
        """
        返回由事务组成的项列表.
        """
        return sorted(self.__items)

    @staticmethod
    def create(transactions):
        """
        创建TransactionManager实例.
        如果给定实例就是TransactionManager实例，则返回本身
        """
        if isinstance(transactions, TransactionManager):
            return transactions
        return TransactionManager(transactions)


# 忽略名称错误，因为这些名称属于名称元组.
SupportRecord = namedtuple( # pylint: disable=C0103
    'SupportRecord', ('items', 'support'))
RelationRecord = namedtuple( # pylint: disable=C0103
    'RelationRecord', SupportRecord._fields + ('ordered_statistics',))
OrderedStatistic = namedtuple( # pylint: disable=C0103
    'OrderedStatistic', ('items_base', 'items_add', 'confidence', 'lift',))


################################################################################
# 内部函数.
################################################################################
def create_next_candidates(prev_candidates, length):
    """
    以列表的形式返回apriori候选项

    :param
        prev_candidates -- 以列表形式的以前候选项.
        length -- 下一个候选想的长度.
    """
    # 处理项并排序.
    item_set = set()
    for candidate in prev_candidates:
        for item in candidate:
            item_set.add(item)
    items = sorted(item_set)

    # 创建暂时的候选项.
    tmp_next_candidates = (frozenset(x) for x in combinations(items, length))

    # 如果下一个候选项的长度为2，则返回所有候选项
    # 因为它们的子集与项相同.
    if length < 3:
        return list(tmp_next_candidates)

    # 过滤所有子集在之前候选项的项.
    next_candidates = [
        candidate for candidate in tmp_next_candidates
        if all(
            True if frozenset(x) in prev_candidates else False
            for x in combinations(candidate, length - 1))
    ]
    return next_candidates


def gen_support_records(transaction_manager, min_support, **kwargs):
    """
    返回给定事务的支持度(support)记录生成器.

    :param
        transaction_manager -- TransactionManager实例.
        min_support -- 最小支持度(support)(float).

    Keyword arguments:
        max_length -- 关系最大长度(integer).
    """
    # 解析参数.
    max_length = kwargs.get('max_length')

    # 用于测试.
    _create_next_candidates = kwargs.get(
        '_create_next_candidates', create_next_candidates)

    # 处理.
    candidates = transaction_manager.initial_candidates()
    length = 1
    while candidates:
        relations = set()
        for relation_candidate in candidates:
            support = transaction_manager.calc_support(relation_candidate)
            if support < min_support:
                continue
            candidate_set = frozenset(relation_candidate)
            relations.add(candidate_set)
            yield SupportRecord(candidate_set, support)
        length += 1
        if max_length and length > max_length:
            break
        candidates = _create_next_candidates(relations, length)


def gen_ordered_statistics(transaction_manager, record):
    """
    将有序统计信息的生成器作为OrderedStatistic实例返回.

    :param
        transaction_manager -- TransactionManager实例.
        record -- SupportRecord实例.
    """
    items = record.items
    for combination_set in combinations(sorted(items), len(items) - 1):
        items_base = frozenset(combination_set)
        items_add = frozenset(items.difference(items_base))
        confidence = (
            record.support / transaction_manager.calc_support(items_base))
        lift = confidence / transaction_manager.calc_support(items_add)
        yield OrderedStatistic(
            frozenset(items_base), frozenset(items_add), confidence, lift)


def filter_ordered_statistics(ordered_statistics, **kwargs):
    """
    过滤OrderedStatistic对象.

    :param
        ordered_statistics -- 可迭代OrderedStatistic对象.

    Keyword arguments:
        min_confidence -- 最小关系置信度值(confidence)(float).
        min_lift -- 最小关系提升度值(lift)(float).
    """
    min_confidence = kwargs.get('min_confidence', 0.0)
    min_lift = kwargs.get('min_lift', 0.0)

    for ordered_statistic in ordered_statistics:
        if ordered_statistic.confidence < min_confidence:
            continue
        if ordered_statistic.lift < min_lift:
            continue
        yield ordered_statistic


################################################################################
# API 函数.
################################################################################
def apriori(transactions, **kwargs):
    """
    执行Apriori算法并返回RelationRecor生成器.

    Arguments:
        transactions -- 可迭代事务对象
                        (eg. [['A', 'B'], ['B', 'C']]).

    Keyword arguments:
        min_support -- 最小关系支持度值(support)(float).
        min_confidence -- 最小关系置信度值(confidence)(float).
        min_lift -- 最小关系提升度值(lift)(float).
        max_length -- 关系最大长度(integer).
    """
    # 解析参数.
    min_support = kwargs.get('min_support', 0.1)
    min_confidence = kwargs.get('min_confidence', 0.0)
    min_lift = kwargs.get('min_lift', 0.0)
    max_length = kwargs.get('max_length', None)

    # 检查参数.
    if min_support <= 0:
        raise ValueError('minimum support must be > 0')

    # 用于测试.
    _gen_support_records = kwargs.get(
        '_gen_support_records', gen_support_records)
    _gen_ordered_statistics = kwargs.get(
        '_gen_ordered_statistics', gen_ordered_statistics)
    _filter_ordered_statistics = kwargs.get(
        '_filter_ordered_statistics', filter_ordered_statistics)

    # 计算支持度.
    transaction_manager = TransactionManager.create(transactions)
    support_records = _gen_support_records(
        transaction_manager, min_support, max_length=max_length)

    # 计算有序统计数据.
    for support_record in support_records:
        ordered_statistics = list(
            _filter_ordered_statistics(
                _gen_ordered_statistics(transaction_manager, support_record),
                min_confidence=min_confidence,
                min_lift=min_lift,
            )
        )
        if not ordered_statistics:
            continue
        yield RelationRecord(
            support_record.items, support_record.support, ordered_statistics)