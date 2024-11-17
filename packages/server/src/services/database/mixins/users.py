# @description: Database mixin for handling user database operations

from typing import Optional
import psycopg2
from psycopg2.errors import UniqueViolation
if TYPE_CHECKING:
    from psycopg2.pool import SimpleConnectionPool


class UsersMixin:
    """
    A collection of methods for handling user database operations.
    """

    connectionPool: "SimpleConnectionPool"

import uuid  # Import Python's UUID library

import uuid  # Ensure UUID import

class UsersMixin:
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


    def get_user(self, uuid: str) -> Optional[dict]:
        """
        Retrieves a user by their UUID.

        Args:
            uuid (str): The UUID of the user.

        Returns:
            Optional[dict]: A dictionary with the user's data if found, None otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE uuid = %s", (uuid,))
                user_data = cursor.fetchone()
                if user_data:
                    column_names = [desc[0] for desc in cursor.description]
                    return dict(zip(column_names, user_data))
                return None
        except Exception as e:
            print("Failed to retrieve user:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def update_user(self, uuid: str, username: Optional[str], password_hash: Optional[str]) -> bool:
        """
        Updates a user's data in the database.

        Args:
            uuid (str): The UUID of the user.
            username (Optional[str]): The new username (if updating).
            password_hash (Optional[str]): The new hashed password (if updating).

        Returns:
            bool: True if successful, False otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                if username and password_hash:
                    cursor.execute(
                        "UPDATE users SET username = %s, password_hash = %s WHERE uuid = %s",
                        (username, password_hash, uuid),
                    )
                elif username:
                    cursor.execute(
                        "UPDATE users SET username = %s WHERE uuid = %s",
                        (username, uuid),
                    )
                elif password_hash:
                    cursor.execute(
                        "UPDATE users SET password_hash = %s WHERE uuid = %s",
                        (password_hash, uuid),
                    )
                else:
                    return False  # No data to update
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print("Failed to update user:", e, flush=True)
            return False
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

    def get_user_by_username(self, username: str) -> Optional[dict]:
        """
        Retrieves a user by their username.

        Args:
            username (str): The username of the user.

        Returns:
            Optional[dict]: A dictionary with the user's data if found, None otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user_data = cursor.fetchone()
                if user_data:
                    column_names = [desc[0] for desc in cursor.description]
                    return dict(zip(column_names, user_data))
                return None
        except Exception as e:
            print("Failed to retrieve user by username:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)
