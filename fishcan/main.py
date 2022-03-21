import os
import random
import datetime

import chess.engine
from flask import Flask

from lyre.clients import LichessClient, AmbrosiaClient
from lyre.analysis import analyse_game

NUM_GAMES = 10

app = Flask(__name__)
ambrosia = AmbrosiaClient()
stockfish = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")


def _ingest_games(num_games: int):
    player = random.choice(ambrosia.get_all_player_names())
    newest_game_timestamp = ambrosia.get_newest_game_time(player)
    if newest_game_timestamp is None:
        newest_game_timestamp = datetime.datetime(1980, 1, 1)
    games = LichessClient.get_games(
        player,
        since=int(newest_game_timestamp.timestamp() * 1000) + 1000,
        max=num_games,
        rated=True,
        perfType="blitz,rapid,classical",
        clocks=True,
        sort="dateAsc")
    processed = 0
    for game in games:
        analysed_game = analyse_game(game, player, stockfish)
        ambrosia.insert_game(analysed_game)
        processed += 1
    if processed < num_games:
        _ingest_games(num_games - processed)


@app.route("/ingest")
def ingest():
    _ingest_games(NUM_GAMES)
    return "Great Success!\nhttps://www.youtube.com/watch?v=r13riaRKGo0"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))