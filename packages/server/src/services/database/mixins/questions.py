# @author: Adi-K527 (Adi Kandakurtikar)
# @description: Database class for handling question database operations

from typing import TYPE_CHECKING

import psycopg2

if TYPE_CHECKING:
    from psycopg2.pool import SimpleConnectionPool


class QuestionsMixin:
    """
    A collection of methods for handling question database operations.
    """

    connectionPool: "SimpleConnectionPool"

    def get_one_question(self, question_id: int) -> dict:
        """
        Retrieves a single question.

        Args:
            question_id (id): The id of the question.

        Returns:
            dict:  A dictionary containing information about the question if successful, None otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Questions WHERE id = %s", (question_id,))
                question_data = cursor.fetchone()
                conn.commit()

                if question_data:
                    column_names = [desc[0] for desc in cursor.description]
                    return [dict(zip(column_names, question_data))]
                else:
                    print("Failed to get the question.", flush=True)
                    return None
        except Exception as e:
            print("Failed to get question:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def get_all_questions(self) -> list[dict]:
        """
        Retrieves all questions.

        Returns:
            list[dict]:  A list of dictionaries containing information about each question if successful, None otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Questions")
                questions_data = cursor.fetchall()

                if questions_data:
                    column_names = [desc[0] for desc in cursor.description]
                    return [dict(zip(column_names, row)) for row in questions_data]
                else:
                    print("Failed to retrieve all questions.", flush=True)
                    return None
        except Exception as e:
            print(f"Error fetching questions: {e}", flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def create_question(self, request) -> dict:
        """
        Creates a new question in the database.

        Args:
            request: The request object containing the attributes of the question.

        Returns:
            dict: A dictionary containing information about the newly created question if successful, None otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Questions (question, difficulty, option1, option2, option3, option4) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *",
                    (
                        request.question,
                        request.difficulty,
                        request.option1,
                        request.option2,
                        request.option3,
                        request.option4,
                    ),
                )
                question_data = cursor.fetchone()
                conn.commit()

                if question_data:
                    column_names = [desc[0] for desc in cursor.description]
                    return [dict(zip(column_names, question_data))]
                else:
                    print(
                        "Failed to retrieve question data after insertion.", flush=True
                    )
                    return None
        except psycopg2.IntegrityError as e:
            # Check if it's a duplicate key error
            if "duplicate key value violates unique constraint" in str(e):
                return None
            else:
                raise e
        except Exception as e:
            print("Failed to create question:", e, flush=True)
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
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Failed to delete question: {e}", flush=True)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)
