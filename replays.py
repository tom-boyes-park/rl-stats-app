import json
import logging
from typing import Dict, List, NamedTuple

import pandas as pd
import streamlit as st
from ballchaser.client import BallChaser


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
    logging.info(f"Searching for replays, params: {json.dumps(params, indent=2)}")
    replay_list = [r for r in _ball_chaser.list_replays(**params)]

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

    def dataframe(self):
        """
        Creates a DataFrame from player statistics dictionaries.
        """
        # unpacks nested stats dict returning column names: level_1.level_2.level_3 etc.
        df = pd.concat([pd.json_normalize(player) for player in self.player_statistics])
        df = df.assign(
            replay_id=self.replay_id, player_id=df["id.platform"] + ":" + df["id.id"]
        )

        # clean up columns
        df.columns = [col.upper().replace(".", "_") for col in df.columns]
        required_cols = [
            "REPLAY_ID",
            "PLAYER_ID",
            "WINNING_TEAM",
            *[col for col in df.columns if col.startswith("STATS_")],
        ]
        df = df[required_cols]

        return df


@st.experimental_memo
def get_replay_stats(_ball_chaser: BallChaser, replay_id: str) -> ReplayStatistics:
    """
    Retrieve player statistics given an instance of BallChaser a replay id.

    Function execution is memoized in order to prevent duplicate API requests for the
    same replay id.

    BallChaser arg is prefixed with an underscore to prevent Streamlit attempting to
    hash the argument.
    """
    logging.info(f"Getting stats for replay: {replay_id}")
    try:
        replay = _ball_chaser.get_replay(replay_id)
    except Exception as e:
        if "not found" in str(e):
            return ReplayStatistics(replay_id, [])
        raise e

    blue_players = replay["blue"]["players"]
    orange_players = replay["orange"]["players"]

    # determine winning team (breaks down for games where there was a draw + forfeit,
    # however we have no other field to determine winning team and this scenario will
    # be rare)
    blue_core_stats = replay["blue"]["stats"]["core"]
    blue_win = blue_core_stats["goals"] > blue_core_stats["goals_against"]

    for player in blue_players:
        player["WINNING_TEAM"] = blue_win

    for player in orange_players:
        player["WINNING_TEAM"] = not blue_win

    return ReplayStatistics(
        replay_id,
        [
            *blue_players,
            *orange_players,
        ],
    )
