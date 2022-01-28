import os

from flask import Flask

from fishcan import Fishcan
from .keys import keys


app = Flask(__name__)
fishcan = Fishcan(
    engine=keys.ENGINE_PATH,
    host=keys.DATABASE_IP,
    database=keys.DATABASE_NAME,
    user=keys.DATABASE_USER,
    password=keys.DATABASE_PASSWORD
)


@app.route("/ingest")
def ingest():
    fishcan.ingest()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))