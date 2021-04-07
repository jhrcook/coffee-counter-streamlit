#!/usr/bin/env python3

"""A Streamlit application for visualizing and analyzing my coffee consumption."""

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
data = deepcopy(_data)

if st.button("Refresh Data"):
    _data.assign(col="hey")
    _data = load_data()

data["date"] = [d.date() for d in data["datetime"]]


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
)

p_num_uses.xaxis.axis_label = "date"
p_num_uses.yaxis.axis_label = "number of cups of coffee"
p_num_uses.line(
    x="date", y="use_id", source=ColumnDataSource(uses_per_day), alpha=0.5, width=3
)
p_num_uses.scatter(x="date", y="use_id", source=ColumnDataSource(uses_per_day), size=7)

st.subheader("Number of cups over time")
st.bokeh_chart(p_num_uses, use_container_width=True)


#### ---- Histogram of uses per day ---- ####
# source: https://docs.bokeh.org/en/latest/docs/gallery/histogram.html

barplot_col1, barplot_col2 = st.beta_columns(2)

BARPLOT_HEIGHT = 300

num_uses = uses_per_day["use_id"].values
hist, edges = np.histogram(num_uses, density=True, bins=5)

p_hist = figure(
    plot_height=BARPLOT_HEIGHT,
    y_range=(0, np.max(hist) * 1.02),
)
p_hist.xaxis.axis_label = "number of cups of coffee"
p_hist.yaxis.axis_label = "frequency"
p_hist.quad(
    top=hist,
    bottom=0,
    left=edges[:-1],
    right=edges[1:],
    fill_color="navy",
    alpha=0.5,
    line_color="white",
)

p_hist.add_tools(
    HoverTool(
        tooltips=[
            ("cups per day", "@left{1.1} - @right{1.1}"),
            ("frequency", "@top{1.11}"),
        ],
    )
)

barplot_col1.subheader("Cups of coffee per day")
barplot_col1.bokeh_chart(p_hist, use_container_width=True)

#### ---- Histogram of uses per bag ---- ####

uses_per_bag = (
    data.groupby(["brand", "name", "bag_id"])["use_id"].count().reset_index(drop=False)
)

use_histogram_df = (
    uses_per_bag.groupby(["use_id"])["bag_id"].count().reset_index(drop=False)
)

p_cups_per_bag = figure(
    plot_height=BARPLOT_HEIGHT,
    y_range=(0, np.max(use_histogram_df.bag_id)),
)

p_cups_per_bag.xaxis.axis_label = "number of cups of coffee"
p_cups_per_bag.yaxis.axis_label = "count"

p_cups_per_bag.vbar(
    x="use_id",
    top="bag_id",
    bottom=0,
    width=1,
    fill_color="navy",
    alpha=0.5,
    line_color="white",
    hover_line_color="navy",
    source=ColumnDataSource(use_histogram_df),
)
p_cups_per_bag.add_tools(
    HoverTool(tooltips=[("num. bags", "@bag_id"), ("num. cups", "@use_id")])
)


barplot_col2.subheader("Cups of coffee per bag")
barplot_col2.bokeh_chart(p_cups_per_bag, use_container_width=True)


#### ---- Interval plot of bag lifetimes ---- ####
# TODO
# x-axis: date
# y-axis: unique bag ("BRCC - Beyond Black")
# For each bag, a bar from its start date to end date.
# source: https://docs.bokeh.org/en/latest/docs/gallery/bar_intervals.html
