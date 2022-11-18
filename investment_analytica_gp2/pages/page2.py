import numpy as np
import pandas as pd
from datetime import date
import yfinance as yf
import pandas_datareader as data
from keras.models import load_model
import streamlit as st

st.markdown("Compare")
st.sidebar.markdown("Compare")

st.title('Comparison')
tickers = pd.read_excel("Companies.xlsx")
symbols = tickers['Symbol'].tolist()

dropdown = st.multiselect('Pick Your Tickers', symbols)

start = st.date_input('Start', value = pd.to_datetime('01-01-2021'))
end = st.date_input('End', value = pd.to_datetime('today'))

def relativeret(df):
    rel = df.pct_change()
    cumret = (1+rel).cumprod() - 1
    cumret = cumret.fillna(0)
    return cumret

if len(dropdown) > 0:
    df = relativeret(yf.download(dropdown,start,end)['Close'])
    st.line_chart(df)