from typing import Dict, Any, List

import requests


class LichessClient:
    """Lichess API Client"""

    def get_user_data(username: str) -> Dict[str, Any]:
        """Get user public data.

        Args:
            username (str): lichess username

        Raises:
            ConnectionError: raised if request status code is not 200

        Returns:
            Dict[str, Any]: json response
        """        
        response = requests.get(
            f"https://lichess.org/api/user/{username}"
        )
        
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
        response = requests.get(f"https://lichess.org/api/user/{username}/rating-history")
        
        if response.status_code == 200:
            return response.json()
        else:
            raise ConnectionError()
