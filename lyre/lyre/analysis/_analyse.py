from datetime import datetime

import chess
from chess.pgn import Game
from chess.engine import SimpleEngine, Limit

from ._analysed_game import AnalysedGame
from ._analysed_move import AnalysedMove
from ._engine_line import EngineLine


def analyse_game(game: Game, player: str, engine: SimpleEngine) -> AnalysedGame:
    analysed_game = _extract_data(game, player)

    white = analysed_game.colour_player == "white"

    moves = [move for move in analysed_game.game.mainline()]
    move_number = 0
    for i in range(0 if white else 1, len(moves), 2):
        move_number += 1
        analysed_move = AnalysedMove()
        analysed_move.move_number = move_number
        analysed_move.move = moves[i].uci()
        analysed_move.board_after = moves[i].board()
        
        if i == 0:
            analysed_move.board_before = chess.Board()
            analysed_move.fen_before = chess.STARTING_FEN
        else:
            analysed_move.move_before = moves[i - 1].uci()
            analysed_move.board_before = moves[i - 1].board()
            analysed_move.fen_before = moves[i - 1].board().fen()
        if i != len(moves) - 1:
            analysed_move.move_after = moves[i + 1].uci()

        engine_analysis_before = engine.analyse(analysed_move.board_before, Limit(depth=16), multipv=3, options={"Analysis Contempt": "Off", "Contempt": "0", "Threads": "4"})
        analysed_move.score_before = engine_analysis_before[0]["score"].relative.score(mate_score=10000)
        analysed_move.board_after = moves[i].board()
        analysed_move.fen_after = moves[i].board().fen()
        engine_analysis_after = engine.analyse(moves[i].board(), Limit(depth=16), options={"Analysis Contempt": "Off", "Contempt": "0", "Threads": "4"})
        analysed_move.score_after = -engine_analysis_after["score"].relative.score(mate_score=10000)
        analysed_move.score_delta = analysed_move.score_after - analysed_move.score_before

        for pv in engine_analysis_before:
            score = pv["score"].relative.score(mate_score=10000)
            if (score - analysed_move.score_after) > -20 and str(pv["pv"][0]) != analysed_move.move:
                engine_line = EngineLine()
                engine_line.score_after = score
                engine_line.score_delta = score - analysed_move.score_after
                engine_line.sequence = [str(move) for move in pv["pv"][:5]]
                analysed_move.engine_lines.append(engine_line)

        analysed_game.moves.append(analysed_move)
    return analysed_game


def _extract_data(game: Game, player: str) -> AnalysedGame:
    analysed_game = AnalysedGame()
    analysed_game.game = game
    analysed_game.pgn = str(game)
    analysed_game.name_player = player.lower()
    analysed_game.source = "lichess"
    analysed_game.opening_eco = game.headers["ECO"]
    analysed_game.time_control_format = game.headers["TimeControl"]
    analysed_game.timestamp = datetime.strptime(
        game.headers["UTCDate"] + " " +
        game.headers["UTCTime"], "%Y.%m.%d %H:%M:%S")
    analysed_game.lichess_id = game.headers["Site"].split("/")[-1]
    analysed_game.ply_count = game.end().ply()

    # Player-specific data extraction
    if game.headers["Black"].lower() == analysed_game.name_player:
        analysed_game.colour_player = "black"
        analysed_game.name_opponent = game.headers["White"]
        analysed_game.elo_player = game.headers["BlackElo"]
        analysed_game.elo_opponent = game.headers["WhiteElo"]
        if game.headers["Result"] == "1-0":
            analysed_game.result = "loss"
        elif game.headers["Result"] == "0-1":
            analysed_game.result = "win"
        elif game.headers["Result"] == "1/2-1/2":
            analysed_game.result = "draw"
        else:
            raise ValueError()
    elif game.headers["White"].lower() == analysed_game.name_player:
        analysed_game.colour_player = "white"
        analysed_game.name_opponent = game.headers["Black"]
        analysed_game.elo_player = game.headers["WhiteElo"]
        analysed_game.elo_opponent = game.headers["BlackElo"]
        if game.headers["Result"] == "1-0":
            analysed_game.result = "win"
        elif game.headers["Result"] == "0-1":
            analysed_game.result = "loss"
        elif game.headers["Result"] == "1/2-1/2":
            analysed_game.result = "draw"
        else:
            raise ValueError()
    else:
        raise ValueError()

    if game.end().board().outcome(claim_draw=True) is not None:
        analysed_game.termination = game.end().board().outcome(
            claim_draw=True).termination.name.lower()
    elif analysed_game.result in ["win", "loss"]:
        analysed_game.termination = "resignation"
    elif analysed_game.result == "draw":
        analysed_game.termination = "draw"
    return analysed_game
