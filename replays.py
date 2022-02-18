import json
from typing import List

from ball_chasing import BallChaser


def get_replay_ids(ball_chaser: BallChaser, params: dict) -> List[str]:
    response = ball_chaser.get_replays(params)

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    replay_list = response.json()["list"]
    if not replay_list:
        raise Exception(f"No replays found, params: {json.dumps(params, indent=4)}")

    return [replay["id"] for replay in replay_list]
