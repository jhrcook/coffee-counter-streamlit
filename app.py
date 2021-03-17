#!/usr/bin/env python3

from copy import deepcopy

import numpy as np
import pandas as pd
import streamlit as st
from bokeh.models.tools import HoverTool
from bokeh.plotting import ColumnDataSource, figure

import coffee_counter as cc

#### ---- App info ---- ####

st.title("Coffee Tracking Analysis")

st.header("A visualization and analysis of my coffee-consumption.")

st.markdown("---")

if st.checkbox("More info"):
    st.markdown(
        """
    **Background:** I have a coffee subscription to [Black Rifle Coffee Company](http://blackriflecoffee.com).
    I currently order two bags of coffee every two weeks.

    **The problem:** Recently, I have noticed that I often finish my two bags before the arrival of my next order.

    **The solution:** To solve this problem, I have collected data on my coffee consumption, specifically, tracking the lifetimes' of coffee bags and when I brew a cup of coffee with each.
    I will then use this data to identify the optimal subscription frequency.

    **Implementation:** I have created a web app (using [FastAPI]() and [Deta]()) to store the data and allow simple and fast access from anywhere.
    I then created a [SwiftBar]() plugin to allow me to [register a cup of coffee from my computers menu bar]() and am working on an iOS application to let me register a cup from my phone.

    ---
    """
    )


@st.cache(show_spinner=True)
def load_data() -> pd.DataFrame:
    coffee_counter = cc.CoffeeCounter()
    coffee_counter.get_coffee_data()
    return coffee_counter.tidy_coffee_data().sort_values(["datetime"], ascending=False)


_data = load_data()
data = deepcopy(_data)

if st.button("Refresh Data"):
    _data.assign(col="hey")
    _data = load_data()

data["date"] = [d.date() for d in data["datetime"]]

# st.write(data)

#### ---- Line plot of uses per day over time ---- ####


uses_per_day = data.groupby(["date"])["use_id"].count().reset_index(drop=False)
uses_per_day["date"] = uses_per_day.date.values.astype(np.datetime64)

hover_tool = HoverTool(
    tooltips=[("date", "@date{%F}"), ("num. uses", "@use_id")],
    formatters={"@date": "datetime"},
    mode="vline",
)

p_num_uses = figure(
    x_axis_type="datetime",
    x_range=(uses_per_day.date[0], uses_per_day.date.values[-1]),
    tools=[hover_tool, "pan,wheel_zoom,zoom_in,zoom_out,box_zoom,reset,tap,save"],
    plot_height=400,
    title="Number of uses of my coffee per day",
)
p_num_uses.xaxis.axis_label = "date"
p_num_uses.yaxis.axis_label = "number of cups of coffee"
p_num_uses.line(
    x="date", y="use_id", source=ColumnDataSource(uses_per_day), alpha=0.5, width=3
)
p_num_uses.scatter(x="date", y="use_id", source=ColumnDataSource(uses_per_day), size=7)
st.bokeh_chart(p_num_uses, use_container_width=True)


#### ---- Histogram of uses per bag ---- ####
# source: https://docs.bokeh.org/en/latest/docs/gallery/histogram.html
# TODO: next to it, add histogram of lifetime of bags.

uses_per_bag = (
    data.groupby(["brand", "name", "bag_id"])["use_id"].count().reset_index(drop=False)
)

num_uses = uses_per_bag["use_id"].values
hist, edges = np.histogram(num_uses, density=True, bins=3)

p_hist = figure(
    plot_height=300,
    y_range=(0, np.max(hist) * 1.02),
    title="Distribution of cups of coffee per bag",
)
p_hist.xaxis.axis_label = "number of cups of coffee"
p_hist.yaxis.axis_label = "count"
p_hist.quad(
    top=hist,
    bottom=0,
    left=edges[:-1],
    right=edges[1:],
    fill_color="navy",
    alpha=0.5,
    line_color="white",
)
st.bokeh_chart(p_hist, use_container_width=True)


#### ---- Interval plot of bag lifetimes ---- ####
# x-axis: date
# y-axis: unique bag ("BRCC - Beyond Black")
# For each bag, a bar from its start date to end date.
# source: https://docs.bokeh.org/en/latest/docs/gallery/bar_intervals.html
