#!/usr/bin/env python3

"""A Streamlit application for visualizing and analyzing my coffee consumption."""

from copy import deepcopy
from datetime import datetime, timedelta
from typing import Dict, Optional

import altair as alt
import pandas as pd
import streamlit as st

import coffee_counter as cc
import informational_text

DEV = False

#### ---- App info ---- ####

st.title("Coffee Tracking Analysis")

st.header("A visualization and analysis of my coffee-consumption.")

more_info_expander = st.beta_expander("More info")
with more_info_expander:
    st.markdown(informational_text.more_info())

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
    label="Days rolling avgerage",
    min_value=1,
    max_value=10,
    value=5,
    step=1,
    format="%d",
)

coffee_uses_per_day = (
    coffee_use_data.groupby("date")[["use_id"]]
    .count()
    .reset_index(drop=False)
    .rename(columns={"use_id": "n_cups"})
)

basic_tooltips = [
    alt.Tooltip("date:T", title="date"),
    alt.Tooltip("n_cups:N", title="num.cups"),
]

cups_over_time_plot = (
    alt.Chart(coffee_uses_per_day)
    .mark_line(opacity=0.5, point=True, strokeDash=[3])
    .encode(
        x="date:T",
        y=alt.Y("n_cups", axis=alt.Axis(title="number of cups")),
    )
    .encode(tooltip=basic_tooltips)
    .interactive()
)

cups_rolling_avg = (
    alt.Chart(coffee_uses_per_day)
    .mark_line(color="red", size=3)
    .transform_window(rolling_mean="mean(n_cups)", frame=[-n_days_avg, n_days_avg])
    .encode(x="date:T", y="rolling_mean:Q")
    .encode(
        tooltip=basic_tooltips
        + [alt.Tooltip("rolling_mean:Q", format=",.2f", title="rolling avg.")]
    )
)

cups_per_day_with_rolling_avg = (cups_over_time_plot + cups_rolling_avg).properties(
    title="Cups of coffee consumed per day"
)
chart_placeholder.altair_chart(cups_per_day_with_rolling_avg, use_container_width=True)

last_week_avg = coffee_uses_per_day[
    coffee_uses_per_day.date >= (datetime.today().date() - timedelta(days=7))
].n_cups.mean()


st.markdown(
    f"""
The plot above shows the number of cups of coffee I've had since I began tracking.
Over the entire {coffee_uses_per_day.shape[0]} days, I have averaged {coffee_uses_per_day["n_cups"].mean():0.2f} cups of coffee per day.
Over the last week, I have averaged {last_week_avg:0.2f} cups.
"""
)

#### ---- Historgrams of uses per day and per bag ---- ####

col1, col2 = st.beta_columns(2)


def altair_histogram(
    df: pd.DataFrame,
    x_title: Optional[str] = "number of cups",
    y_title: Optional[str] = "count",
    title: str = "",
    bin_tooltip: bool = True,
) -> alt.Chart:
    return (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("n_cups:Q", bin=True, title=x_title),
            y=alt.Y("count()", title=y_title),
            tooltip=[
                alt.Tooltip("count():N", title="count"),
                alt.Tooltip("n_cups:N", bin=bin_tooltip, title="num. cups"),
            ],
        )
        .properties(title=title)
    )


with col1:
    cups_per_day_histogram = altair_histogram(
        coffee_uses_per_day,
        x_title="number of cups",
        title="Distribution of cups of coffee per day",
        bin_tooltip=False,
    )
    st.altair_chart(cups_per_day_histogram)

cups_per_bag_df = (
    coffee_use_data.query("active == 0")
    .groupby("bag_id")[["use_id"]]
    .count()
    .reset_index(drop=False)
    .rename(columns={"use_id": "n_cups"})
)

with col2:
    # st.dataframe(cups_per_bag_df)
    cups_per_bag_histogram = altair_histogram(
        cups_per_bag_df,
        x_title="number of cups",
        title="Distribution of cups of coffee per coffee bag",
    )
    st.altair_chart(cups_per_bag_histogram)


#### ---- Horizontal bars showing lifetimes of bags ---- ####

coffee_bag_lifetime_df = (
    coffee_use_data[["bag_id", "name", "weight", "start", "finish", "active"]]
    .drop_duplicates()
    .sort_values(["start", "finish", "name"])
    .reset_index(drop=True)
)

if DEV:
    st.dataframe(coffee_bag_lifetime_df)

bag_id_order = coffee_bag_lifetime_df["bag_id"].values

bag_color_palette: Dict[str, str] = {
    "Beyond Black": "#353232",
    "Coffee or Die": "#6B2121",
    "Escape Goat": "#3FEFAC",
    "Flying Elk": "#FFE94A",
    "Gunship": "silver",
    "Liberty": "red",
    "Magia del Campo": "#4ECE4E",
    "Mind, Body & Soul": "#BA2121",
    "Power Llama": "#3749A2",
    "Silencer Smooth": "#B8CCF2",
    "Space Bear": "#DE9153",
    "Tactisquatch": "#D8553A",
}

bag_color_scale = alt.Scale(
    domain=list(bag_color_palette.keys()), range=list(bag_color_palette.values())
)

bag_lifetime_plot = (
    alt.Chart(coffee_bag_lifetime_df)
    .mark_bar()
    .encode(
        x=alt.X("start", title="lifetime of the bag"),
        x2="finish",
        y=alt.Y(
            "bag_id",
            sort=bag_id_order,
            axis=alt.Axis(labels=False, ticks=False),
            title="individual bags of coffee",
        ),
        color=alt.Color("name", scale=bag_color_scale, title="bag name"),
        tooltip=[alt.Tooltip("name"), alt.Tooltip("start"), alt.Tooltip("finish")],
    )
)

st.altair_chart(bag_lifetime_plot, use_container_width=True)

#### ---- Notes on coffee use and other relevant comments ---- ####

st.markdown("---")

notes_expander = st.beta_expander("Notes", expanded=DEV)
with notes_expander:
    st.markdown(informational_text.notes())

recipes_expander = st.beta_expander("Recipes", expanded=DEV)
with recipes_expander:
    st.markdown(informational_text.recipes())
