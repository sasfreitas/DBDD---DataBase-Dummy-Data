# DBDD---DataBase-Dummy-Data
Fetches any empty DB structure (only MySQL for now) and fills it with dummy but valid data. It also takes care of relationships and dependencies.

---

I decided to write this small program in order to automate a very boring and time consuming task: fill empty databases with random but valid data.
This hasn't been tested thoroughly and most likely you'll find bugs, but I'm going to dedicate some time and put effort on it, since I still have a few
features I'd like to add as well as improvements and fixes I can already think of. This was written in Python 3, so I cannot guarantee compatibility with
versions of Python 2.*. 


## Dependencies

I'm using [PyMySQL](https://github.com/PyMySQL/PyMySQL) to communicate with MySQL server. It's quite easy to use and it follows [PEP 249](https://www.python.org/dev/peps/pep-0249/)
You can download it using pip:

```
# pip install PyMySQL
```

## Usage

The usage is fairly simple. Inside the main directory ( /path/to/DBDD ) you just need to enter the following command on the command line:

```
# python -m dbdd.dbdd
```

This will read the configuration file located in /path/to/DBDD/dbdd/configuration.py. Its content is as follows:


    ADAPTER = "mysql"
    DB_HOST = "127.0.0.1"
    DB_PORT = 3306
    DB_USER = "CHANGE ME"
    DB_PASSWORD = "CHANGE ME"
    DB_NAME = "CHANGE ME"
    DB_CHARSET = "utf8mb4"
    NUMBER_OF_ROWS = 10
    FILL_RELATIONS = True


Once again, no rocket science here. Change the values according to your needs. The setting NUMBER_OF_ROWS specifies how many rows
will be filled on each table. The setting FILL_RELATIONS is not being used for now, but by default all the dependencies are being satisfied.

## Test Suite

Coming soon!

## References

* [Python Documentation](https://docs.python.org/3/)
* [PyMySQL](https://github.com/PyMySQL/PyMySQL)

## License

DBDD is released under MIT License. See LICENSE for more information.