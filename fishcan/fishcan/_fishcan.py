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
