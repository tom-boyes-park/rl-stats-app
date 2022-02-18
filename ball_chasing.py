from requests import Response, Session


class BallChaser:
    """Simple wrapper for replay retrieval endpoints of the ballchasing.com API"""

    __BC_REPLAYS_URL = "https://ballchasing.com/api/replays"

    def __init__(self, api_key: str):
        self.session = Session()
        self.session.headers["Authorization"] = api_key

    def get_replays(self, params) -> Response:
        """Filter and retrieve ballchasing.com replays"""
        return self.session.get(url=self.__BC_REPLAYS_URL, params=params)

    def get_replay_stats(self, replay_id: str) -> Response:
        """Retrieve a given replay’s details and stats"""
        return self.session.get(f"{self.__BC_REPLAYS_URL}/{replay_id}")
