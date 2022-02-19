import json
from typing import List, NamedTuple, Dict

from ball_chasing import BallChaser

import streamlit as st


@st.experimental_memo
def get_replay_ids(_ball_chaser: BallChaser, params: dict) -> List[str]:
    """
    Retrieve list of replay ids given an instance of BallChaser and API request
    parameters.

    Function execution is memoized in order to prevent duplicate API requests for the
    same parameters.

    BallChaser arg is prefixed with an underscore to prevent Streamlit attempting to
    hash the argument.
    """
    response = _ball_chaser.get_replays(params)

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    replay_list = response.json()["list"]
    if not replay_list:
        raise Exception(f"No replays found, params: {json.dumps(params, indent=4)}")

    return [replay["id"] for replay in replay_list]


class ReplayStatistics(NamedTuple):
    """
    replay_id: unique identifier for replay
    player_statistics: list player statistics dictionaries
    """

    replay_id: str
    player_statistics: List[Dict]


@st.experimental_memo
def get_replay_stats(_ball_chaser: BallChaser, replay_id: str) -> ReplayStatistics:
    """
    Retrieve player statistics given an instance of BallChaser a replay id.

    Function execution is memoized in order to prevent duplicate API requests for the
    same replay id.

    BallChaser arg is prefixed with an underscore to prevent Streamlit attempting to
    hash the argument.
    """
    response = _ball_chaser.get_replay_stats(replay_id)

    # replays can be deleted
    if response.status_code == 404:
        return ReplayStatistics(replay_id, [])

    if not response.status_code == 200:
        raise Exception(f"Something went wrong, error: {response.text}")

    response_json = response.json()

    return ReplayStatistics(
        replay_id,
        [
            *response_json["blue"]["players"],
            *response_json["orange"]["players"],
        ],
    )
