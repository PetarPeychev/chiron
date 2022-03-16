import os
import random

import chess
import chess.pgn
import chess.engine
from flask import Flask

from lyre.clients import LichessClient, AmbrosiaClient
from lyre.analysis import analyse_game

NUM_GAMES = 100

app = Flask(__name__)
ambrosia = AmbrosiaClient()
stockfish = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")


@app.route("/ingest")
def ingest():
    player = random.choice(ambrosia.get_all_player_names())
    newest_game_timestamp = ambrosia.get_newest_game_time(player)
    games = LichessClient.get_games(
        player,
        since=int(newest_game_timestamp.timestamp() * 1000),
        max=NUM_GAMES,
        rated=True,
        perfType="blitz,rapid,classical",
        clocks=True,
        sort="dateAsc")
    processed = 0
    for game in games:
        analysed_game = analyse_game(game, stockfish)
        # TODO: to ambrosia
        processed += 1
    if processed < NUM_GAMES:
        ingest(NUM_GAMES - processed)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))