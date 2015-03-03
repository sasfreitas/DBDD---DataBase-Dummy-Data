__author__ = 'pmpro'
# coding=utf-8
from dbdd.configuration import *


class Table(object):
    """
    TODO
    """
    def __init__(self, name, adapter):
        """
        :type name : str
        :param name:
        :type adapter : dbdd.adapter.Adapter
        :param adapter
        """
        self.name = name
        self.fields = {}
        self.strong_dependencies = {}
        self.weak_dependencies = {}
        self.dependents = {}
        self.pending_data = []
        self.fields_order = []
        self.adapter = adapter

    def __str__(self):
        return """
= Name: {}\n
= Fields: {}\n
= Strong Dependencies: {}\n
= Weak Dependencies: {}\n
= Dependents: {}\n
= Pending data: {}\n
= Fields order: {}""".format(
            self.name,
            self.fields,
            self.strong_dependencies,
            self.weak_dependencies,
            self.dependents,
            self.pending_data,
            self.fields_order
        )

    def warm_up(self):
        """
        TODO
        :return:
        """
        self.fields = self.adapter.get_fields(self.name)
        self.strong_dependencies, self.weak_dependencies = self.adapter.get_table_dependencies(self.name)
        self.dependents = self.adapter.get_table_dependents(self.name)

    def get_foreign_key_reference(self, field):
        """
        :type field : str
        :param field:
        :return:
        """
        for table, info in self.strong_dependencies.items():
            for s in info:
                if field in s:
                    return [table, s[0]]

        for table, info in self.weak_dependencies.items():
            for s in info:
                if field == s[1]:
                    return [table, s[0]]

        return None

    def populate_data(self, tables):
        """
        TODO
        :type tables : dict[str,Table]
        :param tables:
        :return:
        """
        if len(self.pending_data) > 0:
            return

        if len(self.strong_dependencies) > 0:
            for _table in self.strong_dependencies:
                tables[_table].populate_data(tables)

        # We need to define the order of the fields
        if len(self.fields_order) == 0:
            for field in self.fields:
                self.fields_order.append(field)

        # And now we can populate the table
        records = []
        for i in range(NUMBER_OF_ROWS):
            data = []
            for f in self.fields_order:
                reference = self.get_foreign_key_reference(f)

                if (reference is not None) and (reference[0] == self.name) and (len(self.pending_data) == 0):
                    data.append(self.fields[f]["Default"])

                elif (reference is not None) and (reference[0] == self.name) and (len(self.pending_data) > 0):
                    data.append(self.pending_data[max(0, i-1)][self.fields_order.index(reference[1])])

                elif (reference is not None) and (reference[0] != self.name):
                    data.append(
                        tables[
                            reference[0]
                        ].pending_data[i][tables[reference[0]].fields_order.index(reference[1])]
                    )

                else:
                    data.append(self.adapter.generate_for_type(self.fields[f]["Type"]))

            t = tuple(data)
            self.pending_data.append(t)
            records.append(t)

        self.adapter.write_records(self.name, records, self.fields_order)