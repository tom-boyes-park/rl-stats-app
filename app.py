import os
from typing import List

import pandas as pd
import streamlit as st
from ball_chasing import BallChaser
from replays import get_replay_ids, get_replay_stats
from stats import stats_comparison_radar, STATISTIC_GROUPS

PLATFORMS = {"Steam": "steam", "PSN": "ps4", "Xbox": "xbox", "Epic Games": "epic"}
PLAYLISTS = ["ranked-duels", "ranked-doubles", "ranked-standard"]


def init_session_state():
    if "ball_chaser" not in st.session_state:
        ball_chaser = BallChaser(os.getenv("BC_API_TOKEN"))
        st.session_state["ball_chaser"] = ball_chaser

    if "replay_ids" not in st.session_state:
        st.session_state["replay_ids"] = []


def title():
    st.title("🚀 Rocket League Gameplay Stats")
    st.caption(
        "_Rocket League is a registered trademark of Psyonix. Trademarks are the "
        "property of their respective owners. Game materials copyright Psyonix. "
        "Psyonix has not endorsed and is not responsible for this site or its content._"
    )


def player_form_callback(player: str, platform: str, playlists: List[str]):
    """
    Retrieves and stores replay ids in session state.
    """
    player_id = f"{PLATFORMS[platform]}:{player}"
    st.session_state.player_id = player_id
    try:
        replay_ids = get_replay_ids(
            st.session_state.ball_chaser,
            params={
                "player-id": player_id,
                "count": 50,
                "sort-by": "replay-date",
                "sort-dir": "desc",
                "playlist": playlists,
            },
        )
        st.session_state.replay_ids = replay_ids
    except Exception as e:
        st.sidebar.error(str(e))


def player_form():
    player = st.sidebar.text_input(
        label="Player ID",
        help="Unique player identifier. For console players, this is simply your "
        "gamer tag. For Steam/Epic players this will be your Steam/Epic ID, not your "
        "display name.",
    )
    platform = st.sidebar.selectbox(label="Platform", options=PLATFORMS.keys())
    playlists = st.sidebar.multiselect(label="Playlists", options=PLAYLISTS)

    st.sidebar.button(
        label="Retrieve Statistics",
        disabled=(not player),
        on_click=player_form_callback,
        args=(player, platform, playlists),
    )


def stats_display():
    if not st.session_state.replay_ids:
        return

    replay_stats = []
    progress_bar = st.progress(0)
    with st.empty():
        for i, replay_id in enumerate(st.session_state.replay_ids):
            st.write(
                f"Retrieving statisitics for replay id: '{replay_id}' "
                f"({i+1}/{len(st.session_state.replay_ids)})"
            )
            progress_bar.progress((i + 1) / len(st.session_state.replay_ids))
            replay_stats.append(
                get_replay_stats(st.session_state.ball_chaser, replay_id).dataframe()
            )

    if replay_stats:
        all_stats_df = pd.concat(replay_stats, ignore_index=True)

        player_stats_df = all_stats_df.loc[
            all_stats_df["PLAYER_ID"].eq(st.session_state.player_id)
        ]

        for group in STATISTIC_GROUPS:
            st.plotly_chart(
                stats_comparison_radar(df=player_stats_df, stats_group=group)
            )


def app():
    title()
    player_form()
    try:
        stats_display()
    except Exception as e:
        st.error(str(e))


def main():
    init_session_state()
    app()


if __name__ == "__main__":
    main()
