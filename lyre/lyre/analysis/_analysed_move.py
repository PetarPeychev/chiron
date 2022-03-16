from __future__ import annotations
from typing import List

from ._engine_line import EngineLine

class AnalysedMove:
    """Analysed player move."""

    def __init__(self) -> AnalysedMove:
        self.board_before = None
        self.board_after = None
        self.move = None
        self.move_before = None
        self.move_after = None
        self.fen_before = None
        self.fen_after = None
        self.score_before = None
        self.score_after = None
        self.score_delta = None
        self.engine_lines: List[EngineLine] = []

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