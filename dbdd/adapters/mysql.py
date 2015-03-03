__author__ = 'pmpro'
# coding=utf-8
import random
import pymysql
import time
import re
import decimal
import sys
from dbdd.configuration import *
from dbdd.adapter import Adapter
from dbdd.types.mysql import *


def get_cursor(func):
    """
    TODO
    :type func : function
    :param func:
    """
    def wrapper(*args, **kwargs):
        args[0].cursor = args[0].connection.cursor(pymysql.cursors.DictCursor)
        return func(*args, **kwargs)

    return wrapper


class MySQL(Adapter):
    """
    TODO
    """
    def connect(self):
        """
        TODO
        :return:
        """
        self.connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            passwd=DB_PASSWORD,
            db=DB_NAME,
            charset=DB_CHARSET
        )

    def get_tables(self, full_info=True):
        """
        TODO
        :param full_info:
        :return:
        """
        self.cursor = self.connection.cursor()
        self.cursor.execute("SHOW TABLES")
        rows = self.cursor.fetchall()
        return [t[0] for t in rows]

    @get_cursor
    def get_fields(self, table_name):
        """
        TODO
        :param table_name:
        :return:
        """
        def _parse_type(_type):
            patterns = [
                r"(enum)\((.+)\)",
                r"(decimal)\((.+)\)(\s+(\w+))?",
                r"(\w+)(\((\d+)\))?(\s+(\w+))?"
            ]

            for pattern in patterns:
                _match = re.search(pattern, _type)
                if _match is None:
                    continue

                if _match.group(1) == "enum":
                    return [
                        "enum",
                        list(map(lambda y: y.strip("'") if "'" in y else int(y), _match.group(2).split(",")))
                    ]
                elif _match.group(1) == "decimal":
                    sign = "unsigned" if _match.group(4) is None else _match.group(4)
                    return ["decimal", sign, list(map(int, _match.group(2).split(",")))]
                elif _match.group(1) in date_formats or _match.group(1) in string_sizes:
                    return [_match.group(1)]
                elif _match.group(1) in variable_strings:
                    return [_match.group(1)] if _match.group(3) is None else [_match.group(1), _match.group(3)]
                elif _match.group(1) in numerical_ranges:
                    return [_match.group(1), "signed"] if _match.group(5) is None else [_match.group(1), _match.group(5)]
                else:
                    return _type

            return _type

        self.cursor.execute("DESCRIBE `{}`".format(table_name))
        rows = self.cursor.fetchall()
        fields = {}
        for f in rows:
            fields[f["Field"]] = {
                "Null": f["Null"],
                "Default": f["Default"],
                "Type": _parse_type(f["Type"]),
                "Extra": f["Extra"]
            }

        return fields

    @get_cursor
    def get_table_dependencies(self, table_name):
        """
        TODO
        :param table_name:
        :return:
        """
        self.cursor.execute("""
    SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
    FROM `INFORMATION_SCHEMA`.`KEY_COLUMN_USAGE`
    WHERE TABLE_NAME = '{}' AND TABLE_SCHEMA = '{}' AND REFERENCED_TABLE_NAME IS NOT NULL""".format(table_name, DB_NAME))
        rows = self.cursor.fetchall()
        strong_dependencies, weak_dependencies = {}, {}
        for d in rows:
            if d["REFERENCED_TABLE_NAME"] == table_name:
                if d["REFERENCED_TABLE_NAME"] not in weak_dependencies:
                    weak_dependencies[d["REFERENCED_TABLE_NAME"]] = set()
                weak_dependencies[d["REFERENCED_TABLE_NAME"]].add(
                    (d["REFERENCED_COLUMN_NAME"], d["COLUMN_NAME"])
                )

            else:
                if d["REFERENCED_TABLE_NAME"] not in strong_dependencies:
                    strong_dependencies[d["REFERENCED_TABLE_NAME"]] = set()
                strong_dependencies[d["REFERENCED_TABLE_NAME"]].add(
                    (d["REFERENCED_COLUMN_NAME"], d["COLUMN_NAME"])
                )

        return strong_dependencies, weak_dependencies

    @get_cursor
    def get_table_dependents(self, table_name):
        """
        :param table_name:
        :return:
        """
        self.cursor.execute("""
    SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
    FROM `INFORMATION_SCHEMA`.`KEY_COLUMN_USAGE`
    WHERE REFERENCED_TABLE_NAME = '{}' AND TABLE_SCHEMA = '{}'""".format(table_name, DB_NAME))
        rows = self.cursor.fetchall()
        dependents = {}
        for d in rows:
            if d["TABLE_NAME"] not in dependents:
                dependents[d["TABLE_NAME"]] = set()
            dependents[d["TABLE_NAME"]].add((d["COLUMN_NAME"], d["REFERENCED_COLUMN_NAME"]))

        return dependents

    def write_records(self, name, records, order):
        """
        TODO
        :type name : str
        :param name :
        :type records : list[tuple]
        :param records:
        :type order : list[str]
        :param order :
        :return:
        """
        self.cursor = self.connection.cursor()
        sql = "INSERT INTO `{}` ({}) VALUES ({})".format(
            name,
            ",".join(list(map(lambda x: "`" + x + "`", order))),
            ", ".join(["%s"] * len(order))
        )
        try:
            self.cursor.executemany(sql, records)
        except:
            print("[ERROR] Unexpected error on table {} with fields {}: {}".format(name, order, sys.exc_info()[0]))
            print("[ERROR] Records: {}".format(records))
            self.connection.rollback()
            raise
        else:
            self.connection.commit()
            print("[DEBUG] Inserted {} rows on table {}".format(NUMBER_OF_ROWS, name))

    @staticmethod
    def generate_for_type(_type):
        """
        :type _type : list
        :param _type:
        :return:
        """
        if _type[0] in numerical_ranges:
            if _type[0] in random_ints:
                return random.randrange(
                    numerical_ranges[_type[0]][_type[1]][0], numerical_ranges[_type[0]][_type[1]][1]
                )
            else:
                return random.uniform(
                    numerical_ranges[_type[0]][0], numerical_ranges[_type[0]][1]
                )

        elif _type[0] == "decimal":
            denominator = 10**_type[2][1]
            upper = 10**(_type[2][0]-_type[2][1])
            lower = 0 if _type[1] == "unsigned" else -upper
            return float(decimal.Decimal(random.randrange(lower, upper))/denominator)

        elif _type[0] in string_sizes:
            return "".join(random.SystemRandom().choice(LIST_OF_CHARS) for _ in range(string_sizes[_type[0]]))

        elif _type[0] in variable_strings:
            return "".join(random.SystemRandom().choice(LIST_OF_CHARS) for _ in range(int(_type[1])))

        elif _type[0] in date_formats:
            return time.strftime(date_formats[_type[0]])

        elif _type[0] == "enum":
            return _type[1][random.randrange(len(_type[1]))]

        else:
            return None