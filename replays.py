import json
from typing import List

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
