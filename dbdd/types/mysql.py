__author__ = 'pmpro'
# coding=utf-8
import string

# http://dev.mysql.com/doc/refman/5.6/en/integer-types.html
numerical_ranges = {
    "tinyint": {
        "signed": [-128, 127],
        "unsigned": [0, 255]
    },
    "smallint": {
        "signed": [-32768, 32767],
        "unsigned": [0, 65535]
    },
    "mediumint": {
        "signed": [-8388608, 8388607],
        "unsigned": [0, 16777215]
    },
    "int": {
        "signed": [-2147483648, 2147483647],
        "unsigned": [0, 4294967295]
    },
    "bigint": {
        "signed": [-9223372036854775808, 9223372036854775807],
        "unsigned": [0, 18446744073709551615]
    },
    "float": [-3.402823466e38, 3.402823466e38],
    "double": [-1.7976931348623157e308, 1.7976931348623157e308]
}

random_ints = ["tinyint", "smallint", "mediumint", "int", "bigint"]

# http://dev.mysql.com/doc/refman/5.6/en/string-type-overview.html
# For future reference: http://www.cl.cam.ac.uk/~mgk25/ucs/examples/UTF-8-test.txt
# _string_sizes = {
#     "tinyblob": 255,
#     "tinytext": 255,
#     "mediumblob": 16777215,
#     "mediumtext": 16777215,
#     "longblob": 4294967295,
#     "longtext": 4294967295
# }

string_sizes = {
    "tinyblob": 10,
    "tinytext": 10,
    "mediumblob": 10,
    "mediumtext": 10,
    "longblob": 10,
    "longtext": 10
}

# _variable_strings = {
#     "char": 255,
#     "varchar": 65535,
#     "binary": 255,
#     "varbinary": 65535,
#     "blob": 65535,
#     "text": 65535
# }

variable_strings = {
    "char": 10,
    "varchar": 10,
    "binary": 10,
    "varbinary": 10,
    "blob": 10,
    "text": 10
}

LIST_OF_CHARS = string.ascii_letters + string.digits + string.punctuation

# http://dev.mysql.com/doc/refman/5.6/en/date-and-time-types.html
date_formats = {
    "date": "%Y-%m-%d",
    "time": "%Y-%m-%d %H:%M:%S",
    "datetime": "%Y-%m-%d %H:%M:%S",
    "timestamp": "%Y-%m-%d %H:%M:%S",
    "year": "%Y"
}