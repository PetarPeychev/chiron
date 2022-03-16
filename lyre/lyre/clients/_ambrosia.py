from datetime import datetime
from typing import List, Dict, Any, Optional

from google.cloud import bigquery


class AmbrosiaClient:
    """Ambrosia OLAP data warehouse client."""

    def __init__(self):
        self._bigquery = bigquery.Client()
        self._cached_queries: Dict[str, Any] = {}

    def get_all_player_names(self) -> List[str]:
        """Get all distinct player names. 

        Returns:
            List[str]: List of all distinct player names.
        """        
        if "all_player_names" not in self._cached_queries:
            query_job = self._bigquery.query("""
                SELECT * 
                FROM EXTERNAL_QUERY(
                    "projects/chiron-chess/locations/europe-west6/connections/nectar",
                    "SELECT DISTINCT(username) FROM chi_lichessaccount;"
                );
                """)
            self._cached_queries["all_player_names"] = [row["username"] for row in query_job]
        return self._cached_queries["all_player_names"]

    def get_newest_game_time(self, player_name: str) -> Optional[datetime]:
        """Get the time of the newest game played by a player.

        Args:
            player_name (str): Player name.

        Returns:
            Optional[datetime]: Timestamp of the newest game or None.
        """        
        query_job = self._bigquery.query(f"""
            SELECT `timestamp` 
            FROM `chiron-chess.facts.game`
            WHERE name_player = "{player_name}"
            ORDER BY `timestamp` DESC
            LIMIT 1
            """)
        results = [row for row in query_job]
        if len(results) > 0:
            return results[0].timestamp
        else:
            return None
