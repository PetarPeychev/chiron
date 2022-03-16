import io
from typing import Dict, Any, List

import requests
import chess
import chess.pgn


class LichessClient:
    """Lichess API Client."""

    def get_user_data(username: str) -> Dict[str, Any]:
        """Get user public data.

        Args:
            username (str): lichess username

        Raises:
            ConnectionError: raised if request status code is not 200

        Returns:
            Dict[str, Any]: json response
        """
        response = requests.get(f"https://lichess.org/api/user/{username}")

        if response.status_code == 200:
            return response.json()
        else:
            raise ConnectionError()

    def get_user_rating_history(username: str) -> List[Any]:
        """Get user rating history for all game types.

        Args:
            username (str): lichess username

        Raises:
            ConnectionError: raised if request status code is not 200

        Returns:
            List[Any]: json response
        """
        response = requests.get(
            f"https://lichess.org/api/user/{username}/rating-history")

        if response.status_code == 200:
            return response.json()
        else:
            raise ConnectionError()

    def get_performance_statistics(username: str,
                                   time_control: str) -> Dict[str, Any]:
        """Get performance statistics for a single game type.

        Args:
            username (str): lichess username
            time_control (str): time control (blitz, bullet, ...)

        Raises:
            ConnectionError: raised if request status code is not 200

        Returns:
            Dict[str, Any]: json response
        """
        response = requests.get(
            f"https://lichess.org/api/user/{username}/perf/{time_control}")

        if response.status_code == 200:
            return response.json()
        else:
            raise ConnectionError()

    def get_games(username: str, **kwargs: Dict[str, Any]) -> List[chess.pgn.Game]:
        """Get games of a user.

        Args:
            username (str): Lichess username.
            **kwargs: Optional filter parameters.

        Returns:
            List[chess.pgn.Game]: List of games.
        """        
        pgn = io.StringIO(
            requests.get(
                f"https://lichess.org/api/games/user/{username}",
                params=kwargs,
                headers={
                    "Content-type": "application/x-chess-pgn"
                }).content.decode("utf-8"))
        games = []
        game = chess.pgn.read_game(pgn)
        while game is not None:
            games.append(game)
            game = chess.pgn.read_game(pgn)
        return games
