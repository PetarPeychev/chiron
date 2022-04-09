import os
import random
import datetime

import chess.engine
from flask import Flask

from lyre.clients import LichessClient, AmbrosiaClient
from lyre.analysis import analyse_game

NUM_GAMES = 20
MAX_RETRIES = 5

app = Flask(__name__)
ambrosia = AmbrosiaClient()
stockfish = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")


def _ingest_games(num_games: int, max_retries: int):
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
    if len(games) < 1:
        max_retries -= 1
    for game in games:
        try:
            analysed_game = analyse_game(game, player, stockfish)
            ambrosia.insert_game(analysed_game)
            processed += 1
        except Exception as ex:
            print(ex)
    if processed < num_games and max_retries > 0:
        _ingest_games(num_games - processed, max_retries)


@app.route("/ingest")
def ingest():
    _ingest_games(NUM_GAMES, MAX_RETRIES)
    return "Great Success!\nhttps://www.youtube.com/watch?v=r13riaRKGo0"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))