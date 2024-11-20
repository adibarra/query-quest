# @author: adibarra (Alec Ibarra)
# @description: Database class for handling statistics database operations

from typing import TYPE_CHECKING, Optional

from helpers.types import StatisticsDict

if TYPE_CHECKING:
    from psycopg2.pool import SimpleConnectionPool


class StatisticsMixin:
    """
    A collection of methods for handling statistics database operations.
    """

    connectionPool: "SimpleConnectionPool"

    def get_statistics(self, uuid: str) -> Optional[StatisticsDict]:
        """
        Retrieves statistics for a given user. If no statistics entry exists for the user,
        initializes it using the `create_statistics` method.

        Args:
            uuid (str): The UUID of the user whose statistics are being retrieved.

        Returns:
            Optional[StatisticsDict]:
                - A dictionary containing the user's statistics if successful:
                    - "user_uuid" (str): The UUID of the user.
                    - "xp" (int): The user's experience points.
                    - "wins" (int): The user's number of wins.
                    - "losses" (int): The user's number of losses.
                - `None` if an error occurs during the operation.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT user_uuid, xp, wins, losses
                    FROM Statistics
                    WHERE user_uuid = %s
                    """,
                    [uuid],
                )
                result = cursor.fetchone()

                if not result:
                    # Create a new statistics entry if none exists
                    return self.create_statistics(uuid)

                statistics_data = dict(zip([desc[0] for desc in cursor.description], result))
                return StatisticsDict(
                    user_uuid=statistics_data["user_uuid"],
                    xp=statistics_data["xp"],
                    wins=statistics_data["wins"],
                    losses=statistics_data["losses"],
                )
        except Exception as e:
            print("Failed to retrieve statistics:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def create_statistics(self, uuid: str) -> Optional[StatisticsDict]:
        """
        Initializes statistics for a given user with default values (`xp=0, wins=0, losses=0`).

        Args:
            uuid (str): The UUID of the user for whom statistics are being initialized.

        Returns:
            Optional[StatisticsDict]:
                - A dictionary containing the newly created statistics if successful:
                    - "user_uuid" (str): The UUID of the user.
                    - "xp" (int): The user's experience points (default 0).
                    - "wins" (int): The user's number of wins (default 0).
                    - "losses" (int): The user's number of losses (default 0).
                - `None` if an error occurs during the operation.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO Statistics (user_uuid, xp, wins, losses)
                    VALUES (%s)
                    RETURNING *
                    """,
                    [uuid],
                )
                result = cursor.fetchone()
                conn.commit()

                if result:
                    statistics_data = dict(zip([desc[0] for desc in cursor.description], result))
                    return StatisticsDict(
                        user_uuid=statistics_data["user_uuid"],
                        xp=statistics_data["xp"],
                        wins=statistics_data["wins"],
                        losses=statistics_data["losses"],
                    )
                return None
        except Exception as e:
            print("Failed to create statistics:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def update_statistics(
        self,
        uuid: str,
        xp_increment: int = 0,
        wins_increment: int = 0,
        losses_increment: int = 0,
    ) -> bool:
        """
        Updates the statistics for a given user by adding the specified increments to their current values.

        This function ensures the user's statistics entry exists before performing the update.

        Args:
            uuid (str): The UUID of the user whose statistics are being updated.
            xp_increment (int): The amount to add to the user's XP (default is 0).
            wins_increment (int): The number of wins to add to the user's total (default is 0).
            losses_increment (int): The number of losses to add to the user's total (default is 0).

        Returns:
            bool:
                - `True` if the statistics were successfully updated.
                - `False` if an error occurs during the operation.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                current_stats = self.get_statistics(uuid)
                if not current_stats:
                    print(f"Failed to find or initialize statistics for user {uuid}")
                    return False

                cursor.execute(
                    """
                    UPDATE Statistics
                    SET xp = xp + %s,
                        wins = wins + %s,
                        losses = losses + %s
                    WHERE user_uuid = %s
                    """,
                    [xp_increment, wins_increment, losses_increment, uuid],
                )
                conn.commit()

                return cursor.rowcount > 0
        except Exception as e:
            print("Failed to update statistics:", e, flush=True)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)
