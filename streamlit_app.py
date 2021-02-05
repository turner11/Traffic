import re
from pathlib import Path
import streamlit as st
import pandas as pd
import datetime

from __main__ import get_camera_info


def sidebar_inputs():
  # st.sidebar.sliderp
  # st.sidebar.number_input

  # year = st.sidebar.number_input('Year', 2020, now_year, now_year - 1)
  # symbol =  st.sidebar.text_input('Symbol', '').strip()
  camera_data = get_camera_info(camera_id=None)
  camera_data




  df_trades, df_dividends = [post_process_df(df) for df in [df_trades, df_dividends]]
  df_trades.quantity = df_trades.quantity.astype(float)
  return df_trades, df_dividends


def main():

  pd.options.display.float_format = '{:,.2f}'.format
  df_trades, df_dividends = sidebar_inputs()

  if st.checkbox("Show purchases table", False):
    '##### Purchases', df_trades[df_trades.quantity >= 0]

  '##### Sells:', df_trades[df_trades.quantity < 0]
  '##### Dividends', df_dividends
  f'#### Total dividents = ${df_dividends.amount.sum():3f}'



main()
