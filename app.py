#!/usr/bin/env python3

from copy import deepcopy
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
from bokeh.models.layouts import Column
from bokeh.models.tools import HoverTool
from bokeh.plotting import ColumnDataSource, figure, show

import coffee_counter as cc


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

st.write(data)

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

uses_per_bag = (
    data.groupby(["brand", "name", "bag_id"])["use_id"].count().reset_index(drop=False)
)

st.write(uses_per_bag)


# TODO: histogram and density plot of lifetime of bags
# https://docs.bokeh.org/en/latest/docs/gallery/histogram.html

# TODO: something like this showing the span for each bag
# https://docs.bokeh.org/en/latest/docs/gallery/bar_intervals.html
