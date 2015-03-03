__author__ = 'pmpro'
# coding=utf-8


class Adapter(object):
    """
    TODO
    """
    def __init__(self):
        """
        :return:
        """
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        """
        TODO
        :return:
        """
        pass

    def close(self):
        """
        TODO
        :return:
        """
        self.connection.close()

    def get_tables(self, full_info=True):
        """
        Returns a list
        :type full_info : bool
        :param full_info:
        :rtype : list
        :return:
        """
        pass

    def get_fields(self, table_name):
        """
        :type table_name : str
        :param table_name:
        :rtype : dict
        :return:
        """
        pass

    def get_table_dependencies(self, table_name):
        """
        Returns a list with the names of all the tables that the
        current table "depends" on, meaning that the current table
        has Foreign Keys pointing to the retrieved tables.
        :type table_name : str
        :param table_name:
        :rtype : list
        :return:
        """
        pass

    def get_table_dependents(self, table_name):
        """
        Returns a list of all the tables that depend on the current table.
        :param table_name:
        :return:
        """
        pass

    def write_records(self, name, records, order):
        """
        :type name : str
        :param name :
        :type records : list[tuple]
        :param records:
        :type order : list[str]
        :param order :
        :return:
        """
        pass

    @staticmethod
    def generate_for_type(_type):
        """
        Returns a randomly generated value, depending on the type.
        :param _type:
        :return:
        """
        pass