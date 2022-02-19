import pandas as pd

import plotly.express as px


STATISTIC_GROUPS = {
    "core": [
        "STATS_CORE_SHOTS",
        "STATS_CORE_SHOTS_AGAINST",
        "STATS_CORE_GOALS",
        "STATS_CORE_GOALS_AGAINST",
        "STATS_CORE_SAVES",
        "STATS_CORE_ASSISTS",
    ],
    "boost1": [
        "STATS_BOOST_PERCENT_ZERO_BOOST",
        "STATS_BOOST_PERCENT_BOOST_0_25",
        "STATS_BOOST_PERCENT_BOOST_25_50",
        "STATS_BOOST_PERCENT_BOOST_50_75",
        "STATS_BOOST_PERCENT_BOOST_75_100",
        "STATS_BOOST_PERCENT_FULL_BOOST",
        "STATS_BOOST_AVG_AMOUNT",
    ],
    "boost2": [
        "STATS_BOOST_BPM",
        "STATS_BOOST_BCPM",
        "STATS_BOOST_AMOUNT_USED_WHILE_SUPERSONIC",
        "STATS_BOOST_AMOUNT_STOLEN",
    ],
    "movement1": [
        "STATS_MOVEMENT_PERCENT_SLOW_SPEED",
        "STATS_MOVEMENT_PERCENT_BOOST_SPEED",
        "STATS_MOVEMENT_PERCENT_SUPERSONIC_SPEED",
        "STATS_MOVEMENT_PERCENT_GROUND",
        "STATS_MOVEMENT_PERCENT_LOW_AIR",
        "STATS_MOVEMENT_PERCENT_HIGH_AIR",
    ],
}


def plot_statistics(df: pd.DataFrame, stats_group: str):
    # average stat values and pivot
    stats_pivoted = (
        pd.DataFrame(df[STATISTIC_GROUPS[stats_group]].mean(), columns=["value"])
        .rename_axis("statistic")
        .reset_index()
    )
    fig = px.line_polar(
        stats_pivoted,
        r="value",
        theta="statistic",
        hover_name="statistic",
        line_close=True,
    )
    fig.update_traces(fill="toself")

    return fig
