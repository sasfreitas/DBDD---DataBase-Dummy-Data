__author__ = 'pmpro'
from dbdd.adapters import factory
from dbdd.table import Table

tables = {}

with factory() as _adapter:
    _tables = _adapter.get_tables()
    for t in _tables:
        table = Table(t, _adapter)
        tables[t] = table
        tables[t].warm_up()

    for name, table in tables.items():
        table.populate_data(tables)