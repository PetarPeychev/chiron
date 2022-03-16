from datetime import datetime

from chess.pgn import Game
from chess.engine import SimpleEngine, Limit

from ._analysed_game import AnalysedGame
from ._analysed_move import AnalysedMove


def analyse_game(game: Game, player: str, engine: SimpleEngine) -> AnalysedGame:
    analysed_game = _extract_data(game, player)
    last_move = None
    for move in analysed_game.game.mainline():
        analysed_move = AnalysedMove()
        analysed_move.board = move.board()
        info = engine.analyse(analysed_move.board, Limit(time=0.1))
        relative_score = info["score"].white(
        ) if analysed_game.colour_player is "white" else info["score"].black()
        move_score = relative_score.score(mate_score=1000)
        analysed_move.score = move_score
        last_move = analysed_move
        analysed_game.moves.append(analysed_move)
    return analysed_game


def _extract_data(game: Game, player: str) -> AnalysedGame:
    analysed_game = AnalysedGame()
    analysed_game.game = game
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
    elif game.result in ["win", "loss"]:
        analysed_game.termination = "resignation"
    elif game.result == "draw":
        analysed_game.termination = "draw"
    return analysed_game
