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
        self,
        uuid: Optional[str] = None,
        username: Optional[str] = None,
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

                user_data = dict(zip([desc[0] for desc in cursor.description], result))
                return UserDict(
                    uuid=user_data["uuid"],
                    username=user_data["username"],
                    password_hash=user_data["password_hash"],
                )
        except Exception as e:
            print("Failed to retrieve user:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def delete_user(
        self,
        uuid: Optional[str] = None,
        username: Optional[str] = None,
    ) -> bool:
        """
        Deletes a user from the database based on either the provided UUID or username.

        This method deletes a user from the database using either the `uuid` or `username`.
        If the deletion is successful, it returns `True`. If no user matching the provided
        identifier exists or if an error occurs, it returns `False`.

        Args:
            uuid (Optional[str]): The UUID of the user to be deleted. Either this or `username` must be provided.
            username (Optional[str]): The username of the user to be deleted. Either this or `uuid` must be provided.

        Returns:
            bool:
                - `True` if the user was successfully deleted from the database.
                - `False` if no user matching the provided identifier exists or if an error occurs during the deletion process.

        Raises:
            ValueError: If neither `uuid` nor `username` is provided.
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
                        DELETE FROM users
                        WHERE uuid = %s
                        """,
                        [uuid],
                    )
                elif username:
                    cursor.execute(
                        """
                        DELETE FROM users
                        WHERE username = %s
                        """,
                        [username],
                    )
                conn.commit()

                return cursor.rowcount > 0
        except Exception as e:
            print("Failed to delete user:", e, flush=True)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def create_user(
        self,
        username: str,
        password_hash: str,
    ) -> Optional[UserDict]:
        """
        Creates a new user in the database.

        This method inserts a new user into the database with the provided `username` and `password_hash`.
        If the user is created successfully, it returns a `UserDict` containing the user's `uuid` and `username`.
        If an error occurs during the creation process, it returns `None`.

        Args:
            username (str): The username of the new user.
            password_hash (str): The hashed password of the new user.

        Returns:
            Optional[UserDict]:
                - A `UserDict` containing the user's data if the user is created successfully. The dictionary contains:
                    - "uuid" (str): The UUID of the user.
                    - "username" (str): The username of the user.
                    - "password_hash" (str): The hashed password of the user.
                - `None` if the user already exists or if an error occurs.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (uuid, username, password_hash)
                    VALUES (gen_random_uuid(), %s, %s)
                    RETURNING *
                    """,
                    [username, password_hash],
                )
                conn.commit()

                result = cursor.fetchone()
                if not result:
                    return None

                user_data = dict(zip([desc[0] for desc in cursor.description], result))
                return UserDict(
                    uuid=user_data["uuid"],
                    username=user_data["username"],
                    password_hash=user_data["password_hash"],
                )
        except Exception as e:
            print("Failed to create user:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)
