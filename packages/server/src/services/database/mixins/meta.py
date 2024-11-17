# @author: adibarra (Alec Ibarra)
# @description: Database class mixin for handling meta database operations

from typing import TYPE_CHECKING, Any, Dict, List

if TYPE_CHECKING:
    from psycopg2.pool import SimpleConnectionPool

class MetaMixin:
    """
    A collection of methods for handling meta database operations.
    """

    connectionPool: "SimpleConnectionPool"

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        !!! DO NOT USE THIS IN PRODUCTION CODE !!!

        Executes a query on the database and returns the results as a list of dictionaries.

        Args:
            query (str): The SQL query to execute.
            params (tuple): The parameters to pass to the query.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the query results.
        """

        print("!!! DO NOT USE THIS IN PRODUCTION CODE !!!", flush=True)

        conn = None
        result = []

        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if cursor.description:
                    column_names = [desc[0] for desc in cursor.description]
                    result = [
                        dict(zip(column_names, [str(value) for value in row]))
                        for row in cursor.fetchall()
                    ]
                conn.commit()
                return result
        except Exception as e:
            print(f"Failed to execute query ({query[:20]}...)", e, flush=True)
            return result
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def show_tables(self) -> List[str]:
        """
        !!! DO NOT USE THIS IN PRODUCTION CODE !!!

        Retrieves a list of table names from the database.

        Returns:
            List[str]: A list of table names as strings.
        """

        result = self.execute_query("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        return [table["table_name"] for table in result] if result else []
