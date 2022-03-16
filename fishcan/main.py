import os
import random

import chess
import chess.pgn
import chess.engine
from flask import Flask
from google.cloud import bigquery

from lyre import LichessClient, AmbrosiaClient
from fishcan import Game

NUM_GAMES = 100

app = Flask(__name__)
ambrosia = AmbrosiaClient()
stockfish = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")


@app.route("/ingest")
def ingest():
    all_users = ambrosia.get_all_player_names()
    username, lichess_username = random.choice(all_users)
    newest_game_timestamp = ambrosia.get_newest_game_time(lichess_username)
    games = LichessClient.get_games(
        lichess_username,
        since=int(newest_game_timestamp.timestamp() * 1000),
        max=NUM_GAMES,
        rated=True,
        perfType="blitz,rapid,classical",
        clocks=True,
        sort="dateAsc")
    processed = 0
    for pychess_game in games:
        game = Game.from_pychess(pychess_game, username, lichess_username)
        game.analyse(stockfish)
        # game.to_bigquery(self.bigquery)
        processed += 1
    if processed < NUM_GAMES:
        ingest(NUM_GAMES - processed)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))