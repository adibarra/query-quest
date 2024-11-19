# @author: Adi-K527 (Adi Kandakurtikar)
# @description: Database class for handling question and tag associations database operations

from typing import TYPE_CHECKING

import psycopg2

from helpers.types import QuestionTagDict

if TYPE_CHECKING:
    from psycopg2.pool import SimpleConnectionPool


class QuestionTagMixin:
    """
    A collection of methods for handling question and tag associations database operations.
    """

    connectionPool: "SimpleConnectionPool"

    def get_question_tags(self) -> list[dict]:
        """
        Retrieves all tags and associated questions.

        Returns:
            list[dict]: A list of dictionaries containing information about each tag association if successful, an empty list otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM Question_Tags
                    """
                )
                question_tags_data = cursor.fetchall()

                if not question_tags_data:
                    print("No question tags found in the database.", flush=True)
                    return []

                column_names = [desc[0] for desc in cursor.description]
                return [dict(zip(column_names, row)) for row in question_tags_data]
        except Exception as e:
            print(f"Error fetching question tags: {e}", flush=True)
            return []
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def get_question_tag(self, question_id: int, tag_id: int) -> dict | None:
        """
        Retrieves a single question tag association.

        Args:
            tag_id (int): The id of the tag.
            question_id (int): The id of the question.

        Returns:
            dict | None: A dictionary containing information about the question tag if successful, None otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM Question_Tags
                    WHERE question_id = %s
                    AND tag_id = %s
                    """,
                    [question_id, tag_id],
                )
                question_tag_data = cursor.fetchone()

                if not question_tag_data:
                    print(
                        f"No question tag pairing found with (question id, tag id): {(question_id, tag_id)}",
                        flush=True,
                    )
                    return None

                column_names = [desc[0] for desc in cursor.description]
                return dict(zip(column_names, question_tag_data))
        except Exception as e:
            print(
                f"Failed to retrieve question tag {(question_id, tag_id)}: {e}",
                flush=True,
            )
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def create_question_tag(self, question_tag: QuestionTagDict) -> dict | None:
        """
        Assigns a set of tags to a specific question.

        Args:
            question_tag (QuestionTagDict): The object containing the specific question and the tag to be assigned.

        Returns:
            dict: A dictionary containing information about the new question tag if successful, None otherwise.
        """
        conn = None
        try:
            question_id, tag_id = question_tag.question_id, question_tag.tag_id

            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT DISTINCT id
                    FROM Questions
                    """,
                )
                unique_questions = cursor.fetchall()
                unique_questions = set(list([i[0] for i in unique_questions]))

                cursor.execute(
                    """
                    SELECT DISTINCT id
                    FROM Tags
                    """,
                )
                unique_tags = cursor.fetchall()
                unique_tags = set(list([i[0] for i in unique_tags]))

                if question_id not in unique_questions:
                    print(f"No question found with id: {question_id}", flush=True)
                    return None

                if tag_id not in unique_tags:
                    print(f"No tag found with id: {tag_id}", flush=True)
                    return None

                cursor.execute(
                    """
                    INSERT INTO Question_Tags (question_id, tag_id)
                    VALUES (%s, %s)
                    RETURNING *
                    """,
                    [question_id, tag_id],
                )
                new_question_tag = cursor.fetchone()
                conn.commit()

                if not new_question_tag:
                    print("No question tags found in the database.", flush=True)
                    return []

                column_names = [desc[0] for desc in cursor.description]
                return dict(zip(column_names, new_question_tag))
        except psycopg2.IntegrityError as e:
            if "duplicate key value violates unique constraint" in str(e):
                print(f"Duplicate question tag entry: {e}", flush=True)
                return None
            else:
                print(f"Integrity error when assigning tags: {e}", flush=True)
                raise e
        except Exception as e:
            print(f"Failed to assign tags: {e}", flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def delete_question_tag(self, question_id: int, tag_id: int) -> bool:
        """
        Removes a previously assigned tag from a specific question.

        Args:
            question_id (int): The id of the question.
            tag_id (int): The id of the tag.

        Returns:
            bool: True if question tag removal was successful, False otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM Question_Tags
                    WHERE question_id = %s
                    AND tag_id = %s
                    """,
                    [question_id, tag_id],
                )
                conn.commit()
                if cursor.rowcount > 0:
                    print(
                        f"Successfully deleted question tag with (question_id, tag_id): {(question_id, tag_id)}",
                        flush=True,
                    )
                    return True
                else:
                    print(
                        f"No tag found with (question_id, tag_id): {(question_id, tag_id)}",
                        flush=True,
                    )
                    return False
        except Exception as e:
            print(
                f"Failed to delete question tag {(question_id, tag_id)}: {e}",
                flush=True,
            )
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)
