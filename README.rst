==
db
==

Connection and query boilerplate built around mysql.connector.

If no exceptions are raised inside context manager, connection is 
automatically committed upon exiting the context manager. However, 
if the connection is to be held open for extended periods, the user can 
also commit their own transactions using the DataBase.commit property.

Connection parameters are fetched from a configuration file and used 
to establish the connection. Example .cnf file::

    [test_db]
    user = user-name
    password = password1
    database = my-database
    host = 0.0.0.0
    charset = utf8
    ssl_ca = /dir/to/ca.pem
    ssl_cert = /dir/to/client-cert.pem
    ssl_key = /dir/to/client-key.pem
    
    ...
    
There can be multiple sections in the .cnf file enabling DataBase 
objects being created for multiple databases within a single application.

Example Usage:

    >>> import db
    >>> with db.DataBase("db_top_feed") as dbse:
    ...     cur = dbse.execute("SELECT * FROM tbl_top_events LIMIT 1")
    ...     print(cur.fetchone())
    ...
    (1, 92, 'Match Price Model Example Match', 2, datetime.datetime(2022, 7, 14, 14, 27), datetime.datetime(2022, 7, 14, 14, 27), 0)

With dict_cursor:
    >>> import json
    >>> with db.DataBase("db_top_feed") as dbse:
    ...     cur = dbse.execute("SELECT event_id, description  FROM tbl_top_events LIMIT 3", dict_cursor=True)
    ...     print(json.dumps(cur.fetchall(), sort_keys=True, indent=4))
    ...
    [
        {
            "description": "Match Price Model Example Match",
            "event_id": 1
        },
        {
            "description": "child_comp_1",
            "event_id": 2
        },
        {
            "description": "child_comp_2",
            "event_id": 3
        }
    ]

Install
~~~~~~~
If you aren't using Pipenv, you're having a laugh::

    pipenv install git+ssh://git@github.com/5uper5hoot/db.git#egg=db

