import os
from typing import List

import streamlit as st
from ball_chasing import BallChaser
from replays import get_replay_ids

PLATFORMS = {"Steam": "steam", "PSN": "ps4", "Xbox": "xbox", "Epic Games": "epic"}
PLAYLISTS = ["ranked-duels", "ranked-doubles", "ranked-standard"]


def init_session_state():
    if "ball_chaser" not in st.session_state:
        ball_chaser = BallChaser(os.getenv("BC_API_TOKEN"))
        st.session_state["ball_chaser"] = ball_chaser

    if "replay_ids" not in st.session_state:
        st.session_state["replay_ids"] = []


def title():
    st.title("Rocket League Gameplay Statistics")


def caption():
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
    try:
        replay_ids = get_replay_ids(
            st.session_state.ball_chaser,
            params={
                "player-id": player_id,
                "count": 3,  # TODO: revert to 200
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


def app():
    title()
    player_form()
    st.json(st.session_state)
    caption()


def main():
    init_session_state()
    app()


if __name__ == "__main__":
    main()
