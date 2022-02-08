from __future__ import annotations
import pickle
from random import randint
from datetime import datetime

import chess
import chess.pgn
import chess.engine
from google.cloud import bigquery

# PIECE_VALUES = zip([1, 3, 3, 5, 9, 0], chess.PIECE_TYPES)


class Move:

    def __init__(self):
        self.board = None
        self.score = None

    # def material_value(self, colour: chess.Color) -> int:
    #     values = []
    #     for piece in chess.PIECE_TYPES:
    #         values.append(PIECE_VALUES[piece] *
    #                       len(self.board.pieces(piece, colour)))
    #     return sum(values)

    # def piece_count(self, colour: chess.Color) -> int:
    #     values = []
    #     for piece in chess.PIECE_TYPES:
    #         values.append(PIECE_VALUES[piece] *
    #                       len(self.board.pieces(piece, colour)))
    #     return sum(values)

    # def pawn_count(self, colour: chess.Color) -> int:
    #     return self.board.pieces(chess.PAWN, colour)


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
        elif game.pychess_game.headers["White"].lower() == lichess_user.lower(
        ):
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
        moves = {}
        last_move = None
        for pychess_move in self.pychess_game.mainline():
            move = Move()
            move.board = pychess_move.board()
            
            info = engine.analyse(move.board, chess.engine.Limit(time=0.1))
            relative_score = info[
                "score"].white() if self.colour_player is "white" else info[
                    "score"].black()
            move_score = relative_score.score(mate_score=1000)
            move.score = move_score
            
            last_move = move

    def to_bigquery(self, client: bigquery.Client):
        with open("output/" + str(randint(1, 100)), 'wb') as fh:
            pickle.dump(self, fh)
