# @author: adibarra (Alec Ibarra)
# @description: Database class for handling user database operations

from typing import TYPE_CHECKING, Optional

from helpers.types import UserDict

if TYPE_CHECKING:
    from psycopg2.pool import SimpleConnectionPool


class UsersMixin:
    """
    A collection of methods for handling user database operations.
    """

    connectionPool: "SimpleConnectionPool"

    def get_user(
        self, uuid: Optional[str] = None, username: Optional[str] = None
    ) -> Optional[UserDict]:
        """
        Retrieves user details based on either the provided UUID or username.

        This method queries the database for a user associated with the given `uuid` or `username`.
        If a user is found, it returns a `UserDict` containing the user's information. If no user
        is found or an error occurs during the query, it returns `None`.

        Args:
            uuid (Optional[str]): The UUID of the user. Either this or `username` must be provided.
            username (Optional[str]): The username of the user. Either this or `uuid` must be provided.

        Returns:
            Optional[UserDict]:
                - A `UserDict` containing the user's data if the user exists. The dictionary contains:
                    - "uuid" (str): The UUID of the user.
                    - "username" (str): The username of the user.
                    - "password_hash" (str): The hashed password of the user.
                - `None` if the user does not exist or if an error occurs.

        Raises:
            ValueError: If neither `uuid` nor `username` is provided.
            Exception: For errors that may occur during user retrieval (e.g., database connectivity issues).
        """

        if not (uuid or username):
            raise ValueError("Either uuid or username must be provided")

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                if uuid:
                    cursor.execute(
                        """
                        SELECT *
                        FROM users
                        WHERE uuid = %s
                        """,
                        [uuid],
                    )
                elif username:
                    cursor.execute(
                        """
                        SELECT *
                        FROM users
                        WHERE username = %s
                        """,
                        [username],
                    )
                conn.commit()

                result = cursor.fetchone()
                if not result:
                    return None

                # Create a dictionary from the query result
                user_data = dict(zip([desc[0] for desc in cursor.description], result))

                return UserDict(
                    uuid=user_data["uuid"],
                    username=user_data["username"],
                    password_hash=user_data["password_hash"],
                )
        except Exception as e:
            print("Failed to retrieve user due to an unexpected error:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def create_user(self, username: str, password_hash: str) -> Optional[dict]:
        conn = None
        try:
            conn = self.connectionPool.getconn()
            user_uuid = str(uuid.uuid4())  # Generate UUID
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (uuid, username, password_hash) VALUES (%s, %s, %s) RETURNING uuid, username",
                    (user_uuid, username, password_hash),
                )
                user_data = cursor.fetchone()
                conn.commit()
                if user_data:
                    print(f"User created with UUID: {user_data[0]}", flush=True)
                    return {"uuid": user_data[0], "username": user_data[1]}
                return None
        except UniqueViolation:
            print("Username already exists", flush=True)
            return None
        except Exception as e:
            print(f"Failed to create user: {e}", flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def delete_user(self, uuid: str) -> bool:
        """
        Deletes a user from the database.

        Args:
            uuid (str): The UUID of the user.

        Returns:
            bool: True if successful, False otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE uuid = %s", (uuid,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print("Failed to delete user:", e, flush=True)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)
