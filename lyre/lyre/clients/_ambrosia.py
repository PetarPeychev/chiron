from datetime import datetime
from typing import List, Dict, Any, Optional

from google.cloud import bigquery

from lyre.analysis import AnalysedGame, AnalysedMove, EngineLine


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

    def get_opening_blunder_games(self, player_name: str) -> List[AnalysedGame]:
        query_job = self._bigquery.query(f"""
            WITH
                blunders AS (
                    SELECT
                        DISTINCT(lichess_id) AS id
                    FROM
                        `chiron-chess.facts.game`,
                        UNNEST(moves) AS move
                    WHERE
                        move.score_delta < -200
                        AND move.move_number < 7 )
            SELECT
                *
            FROM
                `chiron-chess.facts.game`
            WHERE
                name_player = "{player_name}"
            AND
                lichess_id IN ((
                    SELECT
                    id
                    FROM
                    blunders))
            """)
        results = [row for row in query_job]
        games = self._query_to_games(results)
        return games

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
                "move_number": move.move_number,
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

    def _query_to_games(self, results: List[Any]) -> List[AnalysedGame]:
        games = []
        for result in results:
            game = AnalysedGame()
            game.name_player = result.name_player
            game.name_opponent = result.name_opponent
            game.source = result.source
            game.colour_player = result.colour_player
            game.result = result.result
            game.elo_player = result.elo_player
            game.elo_opponent = result.elo_opponent
            game.timestamp = result.timestamp
            game.time_control_format = result.time_control_format
            game.opening_eco = result.opening_eco
            game.ply_count = result. ply_count
            game.termination = result.termination
            game.lichess_id = result.lichess_id
            game.pgn = result.pgn
            game.moves = []
            for move in result.moves:
                current_move = AnalysedMove()
                current_move.move_number = move["move_number"]
                current_move.move = move["move"]
                current_move.move_before = move["move_before"]
                current_move.move_after = move["move_after"]
                current_move.fen_before = move["fen_before"]
                current_move.fen_after = move["fen_after"]
                current_move.score_before = move["score_before"]
                current_move.score_after = move["score_after"]
                current_move.score_delta = move["score_delta"]
                current_move.engine_lines = []
                for line in move["engine_lines"]:
                    current_line = EngineLine()
                    current_line.score_after = line["score_after"]
                    current_line.score_delta = line["score_delta"]
                    current_line.sequence = line["sequence"]
                    current_move.engine_lines.append(current_line)
                game.moves.append(current_move)
            games.append(game)
        return games