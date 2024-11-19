# @author: Adi-K527 (Adi Kandakurtikar)
# @description: Database class for handling tag database operations

from typing import TYPE_CHECKING

import psycopg2

from helpers.types import TagDict

if TYPE_CHECKING:
    from psycopg2.pool import SimpleConnectionPool


class TagsMixin:
    """
    A collection of methods for handling tag database operations.
    """

    connectionPool: "SimpleConnectionPool"

    def get_tags(self) -> list[dict]:
        """
        Retrieves all tags.

        Returns:
            list[dict]: A list of dictionaries containing information about each tag if successful, an empty list otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM Tags
                    """
                )
                tags_data = cursor.fetchall()

                if not tags_data:
                    print("No tags found in the database.", flush=True)
                    return []

                column_names = [desc[0] for desc in cursor.description]
                return [dict(zip(column_names, row)) for row in tags_data]
        except Exception as e:
            print(f"Error fetching tags: {e}", flush=True)
            return []
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def get_tag(self, tag_id: int) -> dict | None:
        """
        Retrieves a single tag.

        Args:
            tag_id (int): The id of the tag.

        Returns:
            dict | None: A dictionary containing information about the tag if successful, None otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM Tags
                    WHERE id = %s
                    """,
                    [tag_id],
                )
                tag_data = cursor.fetchone()

                if not tag_data:
                    print(f"No tag found with id: {tag_id}", flush=True)
                    return None

                column_names = [desc[0] for desc in cursor.description]
                return dict(zip(column_names, tag_data))
        except Exception as e:
            print(f"Failed to retrieve tag {tag_id}: {e}", flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def create_tag(self, tag: TagDict) -> dict | None:
        """
        Creates a new tag in the database.

        Args:
            tag (TagDict): The object containing the attributes of the tag.

        Returns:
            dict | None: A dictionary containing information about the newly created tag if successful, None otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO Tags (name, description)
                    VALUES (%s, %s)
                    RETURNING *
                    """,
                    [tag.name, tag.description],
                )
                tag_data = cursor.fetchone()
                conn.commit()

                if not tag_data:
                    print("Failed to retrieve tag data after insertion.", flush=True)
                    return None

                column_names = [desc[0] for desc in cursor.description]
                return dict(zip(column_names, tag_data))
        except psycopg2.IntegrityError as e:
            if "duplicate key value violates unique constraint" in str(e):
                print(f"Duplicate question entry: {e}", flush=True)
                return None
            else:
                print(f"Integrity error when creating tag: {e}", flush=True)
                raise e
        except Exception as e:
            print(f"Failed to create tag: {e}", flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def delete_tag(self, tag_id: int) -> bool:
        """
        Deletes a tag from the database.

        Args:
            tag_id (int): The id of the tag.

        Returns:
            bool: True if successful, False otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM Tags
                    WHERE id = %s
                    """,
                    [tag_id],
                )
                conn.commit()
                if cursor.rowcount > 0:
                    print(
                        f"Successfully deleted tag with id: {tag_id}",
                        flush=True,
                    )
                    return True
                else:
                    print(f"No tag found with id: {tag_id}", flush=True)
                    return False
        except Exception as e:
            print(f"Failed to delete tag {tag_id}: {e}", flush=True)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)
