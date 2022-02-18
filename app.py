import os

import streamlit as st

from ball_chasing import BallChaser
from replays import get_replay_ids


def title():
    st.title("Rocket League Gameplay Statistics")


def caption():
    st.caption(
        "_Rocket League is a registered trademark of Psyonix. Trademarks are the "
        "property of their respective owners. Game materials copyright Psyonix. "
        "Psyonix has not endorsed and is not responsible for this site or its content._"
    )


def player_form():
    player_id = st.sidebar.text_input(
        label="Player ID",
        help="Unique player identifier. For console players, this is simply your "
        "gamertag. For Steam/Epic players this will be your Steam/Epic ID, not your "
        "display name.",
    )
    player_platform = st.sidebar.selectbox(
        label="Platform", options=["steam", "ps4", "xbox", "epic"]
    )
    playlists = st.sidebar.multiselect(
        label="Playlists", options=["ranked-duels", "ranked-doubles", "ranked-standard"]
    )

    submit = st.sidebar.button(label="Retrieve Statistics", disabled=(not player_id))
    if submit:
        ball_chaser = BallChaser(os.getenv("BC_API_TOKEN"))
        player_id = f"{player_platform}:{player_id}"
        try:
            replay_ids = get_replay_ids(
                ball_chaser,
                params={
                    "player-id": player_id,
                    "count": 200,
                    "sort-by": "replay-date",
                    "sort-dir": "desc",
                    "playlist": playlists,
                },
            )
            st.sidebar.success(f"Retrieved {len(replay_ids)} replays for {player_id}")
        except Exception as e:
            st.sidebar.error(str(e))


def main():
    title()
    player_form()
    caption()


if __name__ == "__main__":
    main()
