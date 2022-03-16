from __future__ import annotations
from typing import List


class EngineLine:
    """Alternative line suggested by the engine."""

    def __init__(self) -> EngineLine:
        self.score_after = None
        self.score_delta = None
        self.sequence: List[str] = []
