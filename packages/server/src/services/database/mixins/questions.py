# @author: adibarra (Alec Ibarra), Adi-K527 (Adi Kandakurtikar)
# @description: Database class for handling question database operations

from typing import TYPE_CHECKING

import psycopg2

from helpers.types import QuestionWithTagsDict

if TYPE_CHECKING:
    from psycopg2.pool import SimpleConnectionPool


class QuestionsMixin:
    """
    A collection of methods for handling question database operations.
    """

    connectionPool: "SimpleConnectionPool"

    def get_question(self, id: int) -> QuestionWithTagsDict | None:
        """
        Retrieves a single question with its associated tags.

        Args:
            id (int): The id of the question.

        Returns:
            QuestionWithTagsDict | None: A dictionary containing information about the question if successful, None otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT q.id, q.question, q.difficulty, q.option1, q.option2, q.option3, q.option4, qt.tag_id
                    FROM Questions q
                    LEFT JOIN Question_Tags qt ON q.id = qt.question_id
                    WHERE q.id = %s
                    """,
                    [id],
                )
                question_data = cursor.fetchall()

                if not question_data:
                    return None

                question = {
                    "id": question_data[0][0],
                    "question": question_data[0][1],
                    "difficulty": question_data[0][2],
                    "options": [question_data[0][3], question_data[0][4], question_data[0][5], question_data[0][6]],
                    "tags": []
                }

                for row in question_data:
                    if row[7]:
                        question["tags"].append(row[7])

                return QuestionWithTagsDict(
                    id=question["id"],
                    question=question["question"],
                    difficulty=question["difficulty"],
                    options=[opt for opt in question["options"] if opt],
                    tags=question["tags"]
                )
        except Exception as e:
            print("Failed to retrieve question:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)


    def get_questions(self) -> list[QuestionWithTagsDict]:
        """
        Retrieves all questions with their associated tags.

        Returns:
            list[dict]: A list of dictionaries containing information about each question if successful, an empty list otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT q.id, q.question, q.difficulty, q.option1, q.option2, q.option3, q.option4, qt.tag_id
                    FROM Questions q
                    LEFT JOIN Question_Tags qt ON q.id = qt.question_id
                    """
                )
                questions_data = cursor.fetchall()

                if not questions_data:
                    return []

                questions = {}
                for row in questions_data:
                    question_id = row[0]
                    if question_id not in questions:
                        questions[question_id] = {
                            "id": row[0],
                            "question": row[1],
                            "difficulty": row[2],
                            "options": [row[3], row[4], row[5], row[6]],
                            "tags": [],
                        }

                    if row[7]:
                        questions[question_id]["tags"].append(row[7])

                return [
                    QuestionWithTagsDict(
                        id=question["id"],
                        question=question["question"],
                        difficulty=question["difficulty"],
                        options=[opt for opt in question["options"] if opt],
                        tags=question["tags"]
                    )
                    for question in questions.values()
                ]
        except Exception as e:
            print("Error fetching questions:", e, flush=True)
            return []
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    # TODO: broken, needs to handle tags
    def create_question(
        self, question: QuestionWithTagsDict
    ) -> QuestionWithTagsDict | None:
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
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING *
                    """,
                    [
                        question.question,
                        question.difficulty,
                        question.option1,
                        question.option2,
                        question.option3 or None,
                        question.option4 or None,
                    ],
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

    # TODO: broken, needs to handle tags
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
                cursor.execute(
                    """
                    DELETE FROM Questions
                    WHERE id = %s
                    """,
                    [question_id],
                )
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
