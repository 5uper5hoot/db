import configparser
import logging
from pathlib import Path

import backoff
import mysql.connector

LOGGER = logging.getLogger(__name__)

class ConnectError(Exception):
    pass

class DataBase:

    CONN = None

    def __init__(self, db_name, cnf_dir=None):
        if cnf_dir is None:
            cnf_dir = str(Path.home()) + "/.db/db.cnf"
        config = configparser.ConfigParser()
        config.read(cnf_dir)
        self.conn_args = dict(config[db_name])

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is None:
            try:
                self.CONN.commit()
            except AttributeError:
                # if called before connect
                pass
            except mysql.connector.errors.InternalError as e:
                if e.msg == "Unread result found":
                    pass
        self.close()

    @backoff.on_exception(backoff.expo,
                          ConnectError,
                          max_tries=5)
    def connect(self):
        try:
            self.CONN = mysql.connector.connect(**self.conn_args)
        except (mysql.connector.errors.InterfaceError,
                mysql.connector.errors.OperationalError,
                mysql.connector.errors.ProgrammingError):
            raise ConnectError

    def close(self):
        try:
            self.CONN.close()
        except AttributeError:
            # if close called before connect
            pass

    @backoff.on_exception(backoff.expo,
                          (mysql.connector.errors.InterfaceError,
                           mysql.connector.errors.OperationalError),
                          max_tries=5)
    def execute(self, sql, data=None, many=False, dict_cursor=False):

        if self.CONN is None:
            self.connect()
        try:
            cursor = self.CONN.cursor(dictionary=dict_cursor)
        except (mysql.connector.errors.OperationalError) as e:
            if e.msg == "MySQL Connection not available.":
                self.CONN = None
            raise

        args = [sql, data] if data else [sql]
        func = cursor.executemany if many else cursor.execute
        func(*args)
        return cursor
