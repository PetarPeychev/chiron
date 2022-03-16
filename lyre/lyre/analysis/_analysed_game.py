from __future__ import annotations
from typing import List

from ._analysed_move import AnalysedMove

class AnalysedGame:
    """Analysed player game."""

    def __init__(self) -> AnalysedGame:
        self.game = None
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
        self.pgn = None
        self.moves: List[AnalysedMove] = []