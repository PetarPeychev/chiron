from datetime import datetime
from typing import List, Dict, Any, Optional

from google.cloud import bigquery

from lyre.analysis import AnalysedGame


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
            self._cached_queries["all_player_names"] = [
                row["username"] for row in query_job]
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

    def insert_game(self, game: AnalysedGame):
        """Insert a new analysed game into the data warehouse.

        Args:
            game (AnalysedGame): Analysed game.
        """
        rows = [{
            "name_player": game.name_player,
            "name_opponent": game.name_opponent,
            "source": game.source,
            "colour_player": game.colour_player,
            "result": game.result,
            "elo_player": game.elo_player,
            "elo_opponent": game.elo_opponent,
            "timestamp": str(game.timestamp),
            "time_control_format": game.time_control_format,
            "opening_eco": game.opening_eco,
            "ply_count": game.ply_count,
            "termination": game.termination,
            "lichess_id": game.lichess_id,
            "pgn": game.pgn,
            "moves": []
        }]

        for move in game.moves:
            move_row = {
                "move": move.move,
                "move_before": move.move_before,
                "move_after": move.move_after,
                "fen_before": move.fen_before,
                "fen_after": move.fen_after,
                "score_before": move.score_before,
                "score_after": move.score_after,
                "score_delta": move.score_delta,
                "engine_lines": []
            }

            for line in move.engine_lines:
                line_row = {
                    "score_after": line.score_after,
                    "score_delta": line.score_delta,
                    "sequence": line.sequence
                }
                move_row["engine_lines"].append(line_row)

            rows[0]["moves"].append(move_row)

        self._bigquery.insert_rows_json("chiron-chess.facts.game", rows)
