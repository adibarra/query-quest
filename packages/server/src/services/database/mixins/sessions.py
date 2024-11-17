# @author: adibarra (Alec Ibarra)
# @description: Database class for handling session database operations

from typing import TYPE_CHECKING, Optional
from helpers.types import SessionDict

if TYPE_CHECKING:
    from psycopg2.pool import SimpleConnectionPool

class SessionsMixin:
    """
    A collection of methods for handling session database operations.
    """

    connectionPool: "SimpleConnectionPool"


    def get_session(self, user_uuid: Optional[str] = None, token: Optional[str] = None) -> Optional[SessionDict]:
        """
        Retrieves the session details based on either the provided session token or the user UUID.

        This method queries the database for a session associated with the given `token` or `user_uuid`.
        If a session is found, it returns a `SessionDict` containing the session information. If no session
        is found or an error occurs during the query, it returns `None`.

        Args:
            user_uuid (Optional[str]): The UUID of the session owner (user). Either this or `token` must be provided.
            token (Optional[str]): The session token. Either this or `user_uuid` must be provided.

        Returns:
            Optional[SessionDict]:
                - A `SessionDict` containing the session data if the session exists. The dictionary contains:
                    - "user_uuid" (str): The UUID of the session owner (user).
                    - "token" (str): The session token.
                    - "created_at" (datetime): The timestamp when the session was created or updated.
                - `None` if the session does not exist or if an error occurs.

        Raises:
            ValueError: If neither `user_uuid` nor `token` is provided.
            Exception: For errors that may occur during session retrieval (e.g., database connectivity issues).
        """

        if not (user_uuid or token):
            raise ValueError("Either user_uuid or token must be provided")

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                if user_uuid:
                    cursor.execute("SELECT * FROM sessions WHERE user_uuid = %s", (user_uuid,))
                elif token:
                    cursor.execute("SELECT * FROM sessions WHERE token = %s", (token,))
                conn.commit()

                result = cursor.fetchone()
                if not result:
                    return None

                session_data = dict(zip([desc[0] for desc in cursor.description], result))
                return SessionDict(
                    user_uuid=session_data["user_uuid"],
                    token=session_data["token"],
                    created_at=session_data["created_at"],
                )
        except Exception as e:
            print(f"Failed to retrieve session for user_uuid {user_uuid} or token {token}:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)


    def create_session(self, user_uuid: str) -> Optional[SessionDict]:
        """
        Creates a new session in the database for the specified user.

        This method inserts a new session into the `sessions` table or updates the existing session
        if a session already exists for the provided `user_uuid`. The session information, including
        the token and created_at timestamp, is returned as a `SessionDict`.

        Args:
            user_uuid (str): The UUID of the user for whom the session is being created.

        Returns:
            Optional[SessionDict]:
                - A `SessionDict` containing the session data if the creation or update was successful.
                  The dictionary contains:
                    - "user_uuid" (str): The UUID of the session owner (user).
                    - "token" (str): The generated or updated session token.
                    - "created_at" (datetime): The timestamp when the session was created or updated.
                - `None` if the operation failed.

        Raises:
            Exception: For errors that may occur during session creation (e.g., database connectivity issues).
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO sessions (user_uuid) VALUES (%s) ON CONFLICT (user_uuid) DO UPDATE SET token = DEFAULT, created_at = DEFAULT RETURNING *",
                    (user_uuid,),
                )
                conn.commit()

                result = cursor.fetchone()
                if not result:
                    return None

                session_data = dict(zip([desc[0] for desc in cursor.description], result))
                return SessionDict(
                    user_uuid=session_data["user_uuid"],
                    token=session_data["token"],
                    created_at=session_data["created_at"],
                )
        except Exception as e:
            print("Failed to create session due to an unexpected error:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)


    def delete_session(self, user_uuid: Optional[str] = None, token: Optional[str] = None) -> bool:
        """
        Deletes an existing session from the database using either the provided session token or the user UUID.

        This method attempts to delete a session from the database based on either the `token` or the `user_uuid`.
        If either parameter is provided, the session will be deleted. The method commits the transaction and returns
        `True` if the deletion is successful. If no session is found or an error occurs during the process, it returns `False`.

        Args:
            user_uuid (Optional[str]): The UUID of the session owner (user) whose session is to be deleted.
            token (Optional[str]): The session token of the session to be deleted.

        Returns:
            bool:
                - `True` if the session was successfully deleted (either by matching the `user_uuid` or `token`).
                - `False` if the session could not be deleted due to an error or if no session was found.

        Raises:
            ValueError: If neither `user_uuid` nor `token` is provided.
            Exception: For errors that may occur during session deletion (e.g., database connectivity issues).
        """

        if not (user_uuid or token):
            raise ValueError("Either `user_uuid` or `token` must be provided")

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                if user_uuid:
                    cursor.execute("DELETE FROM sessions WHERE user_uuid = %s", (user_uuid,))
                elif token:
                    cursor.execute("DELETE FROM sessions WHERE token = %s", (token,))
                conn.commit()

                return cursor.rowcount > 0
        except Exception as e:
            print(f"Failed to delete session due to an unexpected error: {e}", flush=True)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)
