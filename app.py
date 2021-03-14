#!/usr/bin/env python3

from copy import deepcopy
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
from bokeh.plotting import ColumnDataSource, figure, show

import coffee_counter as cc


@st.cache(show_spinner=True)
def load_data() -> pd.DataFrame:
    coffee_counter = cc.CoffeeCounter()
    coffee_counter.get_coffee_data()
    return coffee_counter.tidy_coffee_data()


_data = load_data()
data = deepcopy(_data)

if st.button("Refresh Data"):
    _data.assign(col="hey")
    _data = load_data()

data["date"] = [d.date() for d in data["datetime"]]

st.write(data)

uses_per_day = data.groupby(["date"])["use_id"].count().reset_index(drop=False)


st.write(uses_per_day)

uses_per_day["date"] = uses_per_day.date.values.astype(np.datetime64)

p_num_uses = figure(
    x_axis_type="datetime", x_range=(uses_per_day.date[0], uses_per_day.date.values[-1])
)
p_num_uses.line(x="date", y="use_id", source=ColumnDataSource(uses_per_day))
st.bokeh_chart(p_num_uses)

uses_per_bag = (
    data.groupby(["brand", "name", "bag_id"])["use_id"].count().reset_index(drop=False)
)
st.write(uses_per_bag)

# TODO: histogram and density plot of lifetime of bags
# https://docs.bokeh.org/en/latest/docs/gallery/histogram.html

# TODO: something like this showing the span for each bag
# https://docs.bokeh.org/en/latest/docs/gallery/bar_intervals.html

# DEMO BOKEH PLOT FROM STREAMLIT DOC
# x = [1, 2, 3, 4, 5]
# y = [6, 7, 2, 4, 5]
# p = figure(title='simple line example',x_axis_label='x',y_axis_label='y')
# p.line(x, y)
# st.bokeh_chart(p, use_container_width=True)
