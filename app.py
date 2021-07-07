#!/usr/bin/env python3

"""A Streamlit application for visualizing and analyzing my coffee consumption."""

from copy import deepcopy
from datetime import datetime

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

import coffee_counter as cc

DEV = True

#### ---- App info ---- ####

st.title("Coffee Tracking Analysis")

st.header("A visualization and analysis of my coffee-consumption.")

more_info_expander = st.beta_expander("More info")
with more_info_expander:
    st.markdown(
        """
    **Background:** I have a coffee subscription to [Black Rifle Coffee Company](http://blackriflecoffee.com).
    I currently order two bags of coffee every two weeks.

    **The problem:** Recently, I have noticed that I often finish my two bags before the arrival of my next order.

    **The solution:** To solve this problem, I have collected data on my coffee consumption, specifically, tracking the lifetimes' of coffee bags and when I brew a cup of coffee with each.
    I will then use this data to identify the optimal subscription frequency.

    **Implementation:** I have created a [web API](https://a7a9ck.deta.dev/docs) ([source](https://github.com/jhrcook/coffee-counter-api); using [FastAPI](https://fastapi.tiangolo.com) and [Deta](https://www.deta.sh)) to store the data and allow simple and fast access from anywhere.
    I then created a [SwiftBar](https://swiftbar.app) plugin to allow me to [register a cup of coffee from my computers menu bar](https://github.com/jhrcook/SwiftBar-Plugins/blob/master/coffee-tracker.1h.py) and am working on an iOS application to let me register a cup from my phone.
    """
    )

st.markdown(" ")  # A bit of space between 'More info' and 'Refresh' button.

#### ---- Data ---- ####


@st.cache(show_spinner=True)
def load_data() -> pd.DataFrame:
    coffee_counter = cc.CoffeeCounter()
    coffee_counter.get_coffee_data()
    return coffee_counter.tidy_coffee_data().sort_values(["datetime"], ascending=False)


_data = load_data()
coffee_use_data = deepcopy(_data)

if st.button("Refresh Data"):
    _data.assign(col="hey")
    _data = load_data()

coffee_use_data["date"] = [d.date() for d in coffee_use_data["datetime"]]

coffee_use_data["finish"] = [
    d if d is not None else datetime.today().date() for d in coffee_use_data["finish"]
]

if DEV:
    st.dataframe(coffee_use_data)

#### ---- Line plot of uses per day over time ---- ####

chart_placeholder = st.empty()

n_days_avg = st.slider(
    label="Days rolling avg.", min_value=1, max_value=10, value=5, step=1, format="%d"
)

coffee_uses_per_day = (
    coffee_use_data.groupby("date")[["use_id"]]
    .count()
    .reset_index(drop=False)
    .rename(columns={"use_id": "n_cups"})
)

cups_over_time_plot = (
    alt.Chart(coffee_uses_per_day)
    .mark_line(opacity=0.5, point=True, strokeDash=[3])
    .encode(
        x="date:T",
        y=alt.Y("n_cups", axis=alt.Axis(title="number of cups")),
        tooltip=[alt.Tooltip("n_cups:N", title="num. cups")],
    )
    .interactive()
)

cups_rolling_avg = (
    alt.Chart(coffee_uses_per_day)
    .mark_line(color="red", size=3)
    .transform_window(rolling_mean="mean(n_cups)", frame=[-n_days_avg, n_days_avg])
    .encode(
        x="date:T",
        y="rolling_mean:Q",
        tooltip=[alt.Tooltip("rolling_mean:Q", format=",.2f", title="avg.")],
    )
)

cups_per_day_with_rolling_avg = (cups_over_time_plot + cups_rolling_avg).properties(
    title="Cups of coffee consumed per day"
)

chart_placeholder.altair_chart(cups_per_day_with_rolling_avg, use_container_width=True)

#### ---- Historgrams of uses per day and per bag ---- ####


#### ---- Horizontal bars showing lifetimes of bags ---- ####
