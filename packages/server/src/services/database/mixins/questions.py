# @author: Adi-K527 (Adi Kandakurtikar)
# @description: Database class for handling question database operations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from psycopg2.pool import SimpleConnectionPool


class QuestionsMixin:
    """
    A collection of methods for handling question database operations.
    """

    connectionPool: "SimpleConnectionPool"

    def get_one_question(self, question_id: int) -> dict:
        """
        Fetches a single question based on the question ID.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Questions WHERE id = %s", (question_id,))
                question_data = cursor.fetchone()

                if question_data:
                    column_names = [desc[0] for desc in cursor.description]
                    return dict(zip(column_names, question_data))
                else:
                    return {}
        except Exception as e:
            print(f"Error fetching question {question_id}: {e}", flush=True)
            return {}
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def get_all_questions(self) -> list[dict]:
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Questions")
                questions_data = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                return [dict(zip(column_names, row)) for row in questions_data]
        except Exception as e:
            print(f"Error fetching questions: {e}", flush=True)
            return []
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def create_question(self, request) -> int:
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO Questions (question, difficulty, option1, option2, option3, option4)
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                    """,
                    (
                        request.question,
                        request.difficulty,
                        request.option1,
                        request.option2,
                        request.option3,
                        request.option4,
                    ),
                )
                new_question_id = cursor.fetchone()[0]
                conn.commit()
                return new_question_id
        except Exception as e:
            print(f"Error creating question: {e}", flush=True)
            raise
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def delete_question(self, question_id: int) -> bool:
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM Questions WHERE id = %s", (question_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting question: {e}", flush=True)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)
