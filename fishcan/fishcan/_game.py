from __future__ import annotations
import pickle
from random import randint
from datetime import datetime

import chess
import chess.pgn
import chess.engine
from google.cloud import bigquery


class Game:

    def __init__(self) -> Game:
        self.pychess_game = None
        self.user_id = None
        self.name_player = None
        self.name_opponent = None
        self.source = None
        self.colour_player = None
        self.result = None
        self.elo_player = None
        self.elo_opponent = None
        self.timestamp = None
        self.time_control_format = None
        self.opening_eco = None
        self.ply_count = None
        self.termination = None
        self.lichess_id = None
        self.is_analysed = False

    def from_pychess(pychess_game: chess.pgn.Game, user: str,
                     lichess_user: str) -> Game:
        game = Game()
        game.pychess_game = pychess_game
        game.user_id = user
        game.name_player = lichess_user
        game.source = "lichess"
        game.opening_eco = game.pychess_game.headers["ECO"]
        game.time_control_format = game.pychess_game.headers["TimeControl"]
        game.timestamp = datetime.strptime(
            game.pychess_game.headers["UTCDate"] + " " +
            game.pychess_game.headers["UTCTime"], "%Y.%m.%d %H:%M:%S")
        game.lichess_id = game.pychess_game.headers["Site"].split("/")[-1]
        game.ply_count = game.pychess_game.end().ply()

        # Player-specific data extraction
        if game.pychess_game.headers["Black"].lower() == lichess_user.lower():
            game.colour_player = "black"
            game.name_opponent = game.pychess_game.headers["White"]
            game.elo_player = game.pychess_game.headers["BlackElo"]
            game.elo_opponent = game.pychess_game.headers["WhiteElo"]
            if game.pychess_game.headers["Result"] == "1-0":
                game.result = "loss"
            elif game.pychess_game.headers["Result"] == "0-1":
                game.result = "win"
            elif game.pychess_game.headers["Result"] == "1/2-1/2":
                game.result = "draw"
            else:
                raise ValueError()
        elif game.pychess_game.headers["White"].lower() == lichess_user.lower():
            game.colour_player = "white"
            game.name_opponent = game.pychess_game.headers["Black"]
            game.elo_player = game.pychess_game.headers["WhiteElo"]
            game.elo_opponent = game.pychess_game.headers["BlackElo"]
            if game.pychess_game.headers["Result"] == "1-0":
                game.result = "win"
            elif game.pychess_game.headers["Result"] == "0-1":
                game.result = "loss"
            elif game.pychess_game.headers["Result"] == "1/2-1/2":
                game.result = "draw"
            else:
                raise ValueError()
        else:
            raise ValueError()

        if game.pychess_game.end().board().outcome(
                claim_draw=True) is not None:
            game.termination = game.pychess_game.end().board().outcome(
                claim_draw=True).termination.name.lower()
        elif game.result in ["win", "loss"]:
            game.termination = "resignation"
        elif game.result == "draw":
            game.termination = "draw"

        return game

    def analyse(self, engine: chess.engine.SimpleEngine) -> None:
        pass

    def to_bigquery(self, client: bigquery.Client):
        with open("output/" + str(randint(1, 100)), 'wb') as fh:
            pickle.dump(self, fh)
