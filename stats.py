import pandas as pd

import plotly.graph_objects as go

STATISTIC_GROUPS = {
    "Core": [
        "STATS_CORE_SHOTS",
        "STATS_CORE_SHOTS_AGAINST",
        "STATS_CORE_GOALS",
        "STATS_CORE_GOALS_AGAINST",
        "STATS_CORE_SAVES",
        "STATS_CORE_ASSISTS",
    ],
    "Boost (1)": [
        "STATS_BOOST_PERCENT_ZERO_BOOST",
        "STATS_BOOST_PERCENT_BOOST_0_25",
        "STATS_BOOST_PERCENT_BOOST_25_50",
        "STATS_BOOST_PERCENT_BOOST_50_75",
        "STATS_BOOST_PERCENT_BOOST_75_100",
        "STATS_BOOST_PERCENT_FULL_BOOST",
        "STATS_BOOST_AVG_AMOUNT",
    ],
    "Boost (2)": [
        "STATS_BOOST_BPM",
        "STATS_BOOST_BCPM",
        "STATS_BOOST_AMOUNT_USED_WHILE_SUPERSONIC",
        "STATS_BOOST_AMOUNT_STOLEN",
    ],
    "Movement": [
        "STATS_MOVEMENT_PERCENT_SLOW_SPEED",
        "STATS_MOVEMENT_PERCENT_BOOST_SPEED",
        "STATS_MOVEMENT_PERCENT_SUPERSONIC_SPEED",
        "STATS_MOVEMENT_PERCENT_GROUND",
        "STATS_MOVEMENT_PERCENT_LOW_AIR",
        "STATS_MOVEMENT_PERCENT_HIGH_AIR",
    ],
}


def stats_comparison_radar(df: pd.DataFrame, stats_group: str):
    win_df = df.loc[df["WINNING_TEAM"]]
    loss_df = df.loc[~df["WINNING_TEAM"]]

    win_df_pivoted = (
        pd.DataFrame(win_df[STATISTIC_GROUPS[stats_group]].mean(), columns=["value"])
        .rename_axis("statistic")
        .reset_index()
    )
    loss_df_pivoted = (
        pd.DataFrame(loss_df[STATISTIC_GROUPS[stats_group]].mean(), columns=["value"])
        .rename_axis("statistic")
        .reset_index()
    )

    fig = go.Figure(layout={"title": stats_group})

    fig.add_trace(
        go.Scatterpolar(
            r=win_df_pivoted["value"],
            theta=win_df_pivoted["statistic"],
            fill="toself",
            name="Wins",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=loss_df_pivoted["value"],
            theta=loss_df_pivoted["statistic"],
            fill="toself",
            name="Losses",
        )
    )

    return fig
