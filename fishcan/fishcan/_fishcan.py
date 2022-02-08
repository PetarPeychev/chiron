import io
import random
from typing import List
from datetime import datetime

import chess
import chess.pgn
import chess.engine
import requests
import pg8000.native
from google.cloud import bigquery

from ._chess import Game


class Fishcan:

    def __init__(self, engine: str, host: str, database: str, user: str,
                 password: str) -> None:
        self.database = pg8000.native.Connection(user,
                                                 host=host,
                                                 database=database,
                                                 password=password)
        self.bigquery = bigquery.Client()
        self.engine = chess.engine.SimpleEngine.popen_uci(engine)
        self.cached_queries = {}

    def ingest(self, num_games: int) -> None:
        all_users = self._query_all_users()
        username, lichess_username = random.choice(all_users)
        newest_game_timestamp = self._query_newest_game(username)
        pgn = io.StringIO(
            requests.get(
                f"https://lichess.org/api/games/user/{lichess_username}",
                params={
                    "since": int(newest_game_timestamp.timestamp() * 1000),
                    "max": num_games,
                    "rated": True,
                    "perfType": "blitz,rapid,classical",
                    "clocks": True,
                    "sort": "dateAsc"
                },
                headers={
                    "Content-type": "application/x-chess-pgn"
                }).content.decode("utf-8"))

        processed = 0
        while True:
            pychess_game = chess.pgn.read_game(pgn)
            if pychess_game is not None:
                game = Game.from_pychess(pychess_game, username,
                                         lichess_username)
                game.analyse(self.engine)
                game.to_bigquery(self.bigquery)
                processed += 1
            else:
                break

        if processed < num_games:
            self.ingest(num_games - processed)

    def _query_all_users(self) -> List[List[str]]:
        if "all_users" not in self.cached_queries:
            self.cached_queries["all_users"] = self.database.run("""
                SELECT username, lichess_username 
                FROM users
                """)
        return self.cached_queries["all_users"]

    def _query_newest_game(self, username: str) -> datetime:
        query_job = self.bigquery.query(f"""
            SELECT `timestamp` 
            FROM `chiron-chess.dev.games`
            WHERE user = "{username}"
            ORDER BY `timestamp` DESC
            LIMIT 1
            """)
        results = [row for row in query_job]
        if len(results) > 0:
            return results[0].timestamp
        else:
            return datetime(year=1900, month=1, day=1)

    # def _insert_game(
    #     self,
    #     lichess_id: str,
    #     player_white: str,
    #     player_black: str,
    #     user: str,
    #     result: str,
    #     user_is_white: bool,
    #     elo_white: int,
    #     elo_black: int,
    # ) -> None:
    #     query_job = self.bigquery.query(f"""
    #         INSERT `chiron-chess.dev.games`
    #         VALUES (
    #             "aaaa1111",
    #             "petarpeychev",
    #             "randomnoob",
    #             "petarpeychev",
    #             "1-0",
    #             True,
    #             1400,
    #             1350,
    #             "2022-01-10 01:45:00",
    #             "300+3",
    #             "blitz",
    #             "A45",
    #             3,
    #             "Time forfeit",
    #             [
    #                 ("d4", 0.53, "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1"),
    #                 ("d5", 0.52, "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2"),
    #                 ("Bf4", 0.51, "rnbqkbnr/ppp1pppp/8/3p4/3P1B2/8/PPP1PPPP/RN1QKBNR b KQkq - 1 2")
    #             ]
    #         );
    #         """)
