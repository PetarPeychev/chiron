from __future__ import annotations

import chess.pgn
import chess.engine
from google.cloud import bigquery


class Game:
    def __init__(self, user_id, source, colour_player, ply_count, termination) -> Game:
        self.user_id = user_id
        self.name_player = None
        self.name_opponent = None
        self.source = source
        self.colour_player = colour_player
        self.result = None
        self.elo_player = None
        self.elo_opponent = None
        self.timestamp = None
        self.time_control_format = None
        self.opening_eco = None
        self.ply_count = ply_count
        self.termination = termination
        self.lichess_id = None
        
        self.is_analysed = False

    def from_pychess(game: chess.pgn.Game) -> Game:
        pass
    
    def analyse(engine: chess.engine.SimpleEngine) -> None:
        pass
    
    def to_bigquery(client: bigquery.Client):
        pass