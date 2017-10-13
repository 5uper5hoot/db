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
        LOGGER.debug(f"Looking for config in {cnf_dir}")
        config = configparser.ConfigParser()
        config.read(cnf_dir)
        self.conn_args = dict(config[db_name])

    def __enter__(self):
        LOGGER.debug("Entering DB context manager")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        LOGGER.debug("Exiting DB context manager")
        if exception_type is None:
            LOGGER.debug("No exception passed to __exit__")
            try:
                self.CONN.commit()
                LOGGER.debug("Commit changes")
            except AttributeError:
                # if called before connect
                LOGGER.debug("No established connection")
                pass
            except mysql.connector.errors.InternalError as e:
                if e.msg == "Unread result found":
                    LOGGER.debug("Exiting with unread results")
        self.close()

    @backoff.on_exception(backoff.expo,
                          ConnectError,
                          max_tries=5)
    def connect(self):
        LOGGER.debug("Creating database connection!")
        try:
            self.CONN = mysql.connector.connect(**self.conn_args)
        except (mysql.connector.errors.InterfaceError,
                mysql.connector.errors.OperationalError,
                mysql.connector.errors.ProgrammingError) as e:
            LOGGER.exception(str(e))
            raise ConnectError

    def close(self):
        LOGGER.debug("Attempting to close connection")
        try:
            self.CONN.close()
        except AttributeError:
            # if close called before connect
            LOGGER.debug("No connection to close!")
        else:
            LOGGER.debug("Connection closed")

    @backoff.on_exception(backoff.expo,
                          (mysql.connector.errors.InterfaceError,
                           mysql.connector.errors.OperationalError),
                          max_tries=5)
    def execute(self, sql, data=None, many=False, dict_cursor=False):
        LOGGER.debug(f"execute method called with many: {many},"
                     "dict_cursor: {dict_cursor}")
        if self.CONN is None:
            LOGGER.debug("No established connection!")
            self.connect()
        try:
            cursor = self.CONN.cursor(dictionary=dict_cursor)
        except (mysql.connector.errors.OperationalError) as e:
            LOGGER.exception(str(e))
            if e.msg == "MySQL Connection not available.":
                LOGGER.debug("Connection not available :(")
                self.CONN = None
            raise

        args = [sql, data] if data else [sql]
        func = cursor.executemany if many else cursor.execute
        LOGGER.debug(f"Calling {func} with {args}")
        func(*args)
        return cursor
