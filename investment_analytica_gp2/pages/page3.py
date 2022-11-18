import numpy as np
import pandas as pd
from datetime import date
import yfinance as yf
import pandas_datareader as data
from keras.models import load_model
import streamlit as st
import json
from flask import Flask, jsonify


st.markdown("Predictions")
st.sidebar.markdown("Predictions")

start = '2010-01-01'
end = date.today().strftime("%Y-%m-%d")

df1 = pd.read_excel("Companies.xlsx")
symbols = df1['Symbol']
symbols = symbols.tolist()
user_input = st.text_input("Enter Stock Name", 'GOLD')

df = data.DataReader(user_input , 'yahoo' , start , end)

data_training = pd.DataFrame(df['Close'][0: int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70): int(len(df))])

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range = (0,1))

data_training_array = scaler.fit_transform(data_training)

model = load_model('keras_model.h5')

past_100_days = data_training.tail(100)
final_df = past_100_days.append(data_testing, ignore_index = True)
input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []



for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100: i])
    y_test.append(input_data[i, 0])

x_test, y_test = np.array(x_test) , np.array(y_test)

y_predicted = model.predict(x_test) 
scaler = scaler.scale_

scale_factor = 1/scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor
y_predicted = y_predicted.flatten()

st.subheader('Prediction vs Original')
d2 = {'Close Price' : y_test, 'Prediction': y_predicted}
fig2 = pd.DataFrame(data = d2, columns=['Close Price', 'Prediction'])
st.line_chart(fig2)

length = len(y_predicted)
length2 = len(df['Close'])

if(y_predicted[length - 1] > df['Close'][length2 - 1]):
    st.header("Our Recommendation is to Buy")
else:
    st.header("Our Recommendation is to Sell")
