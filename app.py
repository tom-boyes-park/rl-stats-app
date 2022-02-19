import os

import pandas as pd
import streamlit as st

from ball_chasing import BallChaser
from replays import get_replay_ids, get_replay_stats
from stats import STATISTIC_GROUPS, stats_comparison_radar

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
    st.markdown(
        """
    Enter your profile info in the sidebar and (optionally) filter playlists for which
    to retrieve statistics from replays uploaded to
    [ballchasing.com](https://ballchasing.com/).
    [Radar charts](https://en.wikipedia.org/wiki/Radar_chart) are then plotted comparing
    statistics from wins and losses in your 50 most recent games.
    """
    )


def load_stats():
    """
    Retrieves and stores replay ids in session state.
    """
    player_id = f"{PLATFORMS[st.session_state.platform]}:{st.session_state.player}"
    st.session_state.player_id = player_id

    replay_ids = get_replay_ids(
        st.session_state.ball_chaser,
        params={
            "player-id": player_id,
            "count": 50,
            "sort-by": "replay-date",
            "sort-dir": "desc",
            "playlist": st.session_state.playlists,
        },
    )
    st.session_state.replay_ids = replay_ids


def player_form():
    player = st.sidebar.text_input(
        label="Player ID",
        help="Unique player identifier. For console players, this is simply your "
        "gamer tag. For Steam/Epic players this will be your Steam/Epic ID, not your "
        "display name.",
        key="player",
    )
    st.sidebar.selectbox(label="Platform", options=PLATFORMS.keys(), key="platform")
    st.sidebar.multiselect(label="Playlists", options=PLAYLISTS, key="playlists")

    st.sidebar.button(
        label="Retrieve Statistics",
        disabled=(not player),
        on_click=load_stats,
    )

    st.sidebar.caption(
        "_Rocket League is a registered trademark of Psyonix. Trademarks are the "
        "property of their respective owners. Game materials copyright Psyonix. "
        "Psyonix has not endorsed and is not responsible for this site or its content._"
    )


def stats_display():
    if not st.session_state.replay_ids:
        return

    replay_stats = []
    progress_bar = st.progress(0)
    with st.empty():
        for i, replay_id in enumerate(st.session_state.replay_ids):
            replay_stats.append(
                get_replay_stats(st.session_state.ball_chaser, replay_id).dataframe()
            )
            progress_bar.progress((i + 1) / len(st.session_state.replay_ids))

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
    try:
        player_form()
        stats_display()
    except Exception as e:
        st.error(str(e))
        st.button("Retry", on_click=load_stats)


def main():
    init_session_state()
    app()


if __name__ == "__main__":
    main()
