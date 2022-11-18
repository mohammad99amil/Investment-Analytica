import numpy as np
import pandas as pd
from datetime import date
import yfinance as yf
import pandas_datareader as data
from keras.models import load_model
import json
import streamlit as st
from flask import Flask, jsonify


st.markdown("# Main page")
st.sidebar.markdown("# Main page")

start = '2010-01-01'
end = date.today().strftime("%Y-%m-%d")

df1 = pd.read_excel("Companies.xlsx")
symbols = df1['Symbol']
symbols = symbols.tolist()

st.title('Investment Analytica')

user_input = st.text_input('Enter Stock Name', 'AAPL')
st.header(yf.Ticker(user_input).info['longName'])
st.write(yf.Ticker(user_input).info['longBusinessSummary'])

df = data.DataReader(user_input , 'yahoo' , start , end)
st.subheader('History: 2010 - Today')
st.write(df.loc[ : ,["High", "Low", "Open", "Close"]])

st.subheader('Close Price VS Time') 
st.line_chart(df['Close'])

st.subheader('Close Price VS Time Chart With 100 Days Moving Avg & 200 Days Moving Avg')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
d = {'Close' : df.Close, '100 MA': ma100, '200 MA': ma200 }
fig = pd.DataFrame(data = d, columns=['Close', '100 MA', '200 MA'])
st.line_chart(fig)

#Create API 
ticker = yf.Ticker(user_input)
rec = ticker.recommendations
news = ticker.news

companies_names = df1["Company Name"].tolist()
companies_symbols = df1["Symbol"].tolist()
companies_value = df1['Market Cap'].tolist()
companies_value = [ '%.4f' % elem for elem in companies_value ]

companies_names = json.dumps(companies_names)
companies_symbols = json.dumps(companies_symbols)
companies_value = json.dumps(companies_value)

open_price = df['Open'].tolist()
open_price = [ '%.4f' % elem for elem in open_price ]
json_open_price = json.dumps(open_price)

close_price = df['Close'].tolist()
close_price = [ '%.4f' % elem for elem in close_price ]
json_close_price = json.dumps(close_price)

high_price = df['High'].tolist()
high_price = [ '%.4f' % elem for elem in high_price ]
json_high_price = json.dumps(high_price)

low_price = df['Low'].tolist()
low_price = [ '%.4f' % elem for elem in low_price ]
json_low_price = json.dumps(low_price)

recommendations_firm = rec['Firm'].tolist()
recommendations = rec['To Grade'].tolist()

json_rec_firm = json.dumps(recommendations_firm)
json_rec = json.dumps(recommendations)

json_object = news
title = []
link = []
length = len(json_object)

for i in range(length):
    title.append(json_object[i]["title"])
    link.append(json_object[i]["link"])

title = json.dumps(title)
link = json.dumps(link)

data = {
    'symbols' : companies_symbols,
    'names' : companies_names,
    'values' : companies_value,
    'open_price' : json_open_price,
    'close_price' : json_close_price,
    'high_price' : json_high_price,
    'low_price' : json_low_price,
    'firm_name' : json_rec_firm,
    'recommendations' : json_rec,
    'links' : link,
    'titles' : title,
}

data = json.dumps(data)
#Http Get
app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return jsonify({'data' : data})

if __name__ == '__main__':
    app.run()
