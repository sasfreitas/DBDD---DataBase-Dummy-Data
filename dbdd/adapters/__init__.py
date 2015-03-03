__author__ = 'pmpro'
# coding=utf-8
from dbdd.adapters.mysql import MySQL

MYSQL = 1
POSTGRESQL = 2


def factory(db=MYSQL):
    """
    Factory method only returns MySQL adapter for now.
    :param db:
    :return:
    """
    m = {1: MySQL}
    return None if db not in m else m[db]()