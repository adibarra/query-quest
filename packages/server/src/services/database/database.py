# @author: adibarra (Alec Ibarra)
# @description: Database class for handling database interactions

import os

import psycopg2
from psycopg2 import pool

from config import SERVICE_POSTGRES_URI

# import all mixins here
from services.database.mixins.meta import MetaMixin
from services.database.mixins.questions import QuestionsMixin
from services.database.mixins.sessions import SessionsMixin


# add all imported mixins here
class Database(
    MetaMixin,
    SessionsMixin,
    QuestionsMixin,
    object,
):
    """
    A class representing the database.
    """

    connectionPool: pool.SimpleConnectionPool = None

    def __new__(cls):
        """
        Creates a new instance of the Database class if it doesn't already exist.
        If an instance already exists, returns the existing instance.

        To see the available methods, refer to the mixin classes in the `services.database.mixins` package.

        Returns:
            Database: The Database instance.
        """

        if not hasattr(cls, "instance"):
            conn = None
            cls.instance = super(Database, cls).__new__(cls)

            try:
                print("Connecting to PostgreSQL database...", flush=True)
                cls.instance.connectionPool = pool.SimpleConnectionPool(
                    1, 20, SERVICE_POSTGRES_URI
                )
                print("Connected. Initializing...", flush=True)
                conn = cls.instance.connectionPool.getconn()
                with conn.cursor() as cursor:
                    # Load and execute sql in create.sql
                    with open(
                        os.path.join(os.path.dirname(__file__), "sql", "create.sql"),
                        "r",
                    ) as file:
                        sql_script = file.read()
                        cursor.execute(sql_script)

                    # Load and execute sql in load.sql
                    with open(
                        os.path.join(os.path.dirname(__file__), "sql", "load.sql"), "r"
                    ) as file:
                        sql_script = file.read()
                        cursor.execute(sql_script)

                    # Commit the transaction
                    conn.commit()
                    print("Initialized. Database ready.", flush=True)
            except psycopg2.Error as e:
                print("Failed to initialize database:\n", e, flush=True)
            finally:
                if conn:
                    cls.instance.connectionPool.putconn(conn)

        return cls.instance
