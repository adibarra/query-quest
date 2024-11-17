# @author: Adi-K527 (Adi Kandakurtikar)
# @description: Database class for handling question database operations

from typing import TYPE_CHECKING

import psycopg2

from helpers.types import Question

if TYPE_CHECKING:
    from psycopg2.pool import SimpleConnectionPool


class QuestionsMixin:
    """
    A collection of methods for handling question database operations.
    """

    connectionPool: "SimpleConnectionPool"

    def get_question(self, question_id: int) -> dict | None:
        """
        Retrieves a single question.

        Args:
            question_id (int): The id of the question.

        Returns:
            dict | None: A dictionary containing information about the question if successful, None otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Questions WHERE id = %s", (question_id,))
                question_data = cursor.fetchone()

                if not question_data:
                    print(f"No question found with id: {question_id}", flush=True)
                    return None

                column_names = [desc[0] for desc in cursor.description]
                return dict(zip(column_names, question_data))
        except Exception as e:
            print(f"Failed to retrieve question {question_id}: {e}", flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def get_questions(self) -> list[dict]:
        """
        Retrieves all questions.

        Returns:
            list[dict]: A list of dictionaries containing information about each question if successful, an empty list otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Questions")
                questions_data = cursor.fetchall()

                if not questions_data:
                    print("No questions found in the database.", flush=True)
                    return []

                column_names = [desc[0] for desc in cursor.description]
                return [dict(zip(column_names, row)) for row in questions_data]
        except Exception as e:
            print(f"Error fetching questions: {e}", flush=True)
            return []
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def create_question(self, question: Question) -> dict | None:
        """
        Creates a new question in the database.

        Args:
            question (Question): The object containing the attributes of the question.

        Returns:
            dict | None: A dictionary containing information about the newly created question if successful, None otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO Questions (question, difficulty, option1, option2, option3, option4)
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING *
                    """,
                    (
                        question.question,
                        question.difficulty,
                        question.option1,
                        question.option2,
                        question.option3 or None,
                        question.option4 or None,
                    ),
                )
                question_data = cursor.fetchone()
                conn.commit()

                if not question_data:
                    print(
                        "Failed to retrieve question data after insertion.", flush=True
                    )
                    return None

                column_names = [desc[0] for desc in cursor.description]
                return dict(zip(column_names, question_data))
        except psycopg2.IntegrityError as e:
            if "duplicate key value violates unique constraint" in str(e):
                print(f"Duplicate question entry: {e}", flush=True)
                return None
            else:
                print(f"Integrity error when creating question: {e}", flush=True)
                raise e
        except Exception as e:
            print(f"Failed to create question: {e}", flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def delete_question(self, question_id: int) -> bool:
        """
        Deletes a question from the database.

        Args:
            question_id (int): The id of the question.

        Returns:
            bool: True if successful, False otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM Questions WHERE id = %s", (question_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    print(
                        f"Successfully deleted question with id: {question_id}",
                        flush=True,
                    )
                    return True
                else:
                    print(f"No question found with id: {question_id}", flush=True)
                    return False
        except Exception as e:
            print(f"Failed to delete question {question_id}: {e}", flush=True)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)