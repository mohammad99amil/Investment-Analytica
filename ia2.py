import numpy as np
import pandas as pd
from datetime import date
import yfinance as yf
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st

### to run this program type in the cmd "streamlit run ia2.py" ###


# Define time zone
start = '2010-01-01'
end = date.today().strftime("%Y-%m-%d")

st.title('Investment Analytica')

# take Ticker input from the user
user_input = st.text_input('Enter Stock Name', 'AAPL')

# read data
df = data.DataReader(user_input , 'yahoo' , start , end)
st.subheader('Data from 2010 - Today')
st.write(df.loc[ : ,["High", "Low", "Open", "Close"]])

# recommendations
st.subheader('Analyst Recommendations')
tik = yf.Ticker(user_input)
rec = tik.recommendations
st.write(rec.loc[: , ["Firm", "To Grade"]])

# Ticker News
st.subheader('Articles')
st.write(tik.news)

# Close Prive VS Time Chart
st.subheader('Close VS Time') 
fig = plt.figure(figsize = (12,6))
plt.plot(df.Close)
st.pyplot(fig)

# Close Price VS Time VS 100 days moving average Chart
st.subheader('Close VS Time chart with 100MA')
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)

# Close Price VS Time VS 100 days moving average && 200 days moving average Chart
st.subheader('Close VS Time chart with 100MA & 200MA')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma100, 'r')
plt.plot(ma200, 'g')
plt.plot(df.Close, 'b')
st.pyplot(fig)

# 70% Data training
data_training = pd.DataFrame(df['Close'][0: int(len(df)*0.70)])
# 30% Data testing
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70): int(len(df))])

print(data_training.shape)
print(data_testing.shape)

#import sklearn model 
from sklearn.preprocessing import MinMaxScaler
# make Scaler of the data between 0 & 1
scaler = MinMaxScaler(feature_range = (0,1))

# fit data training
data_training_array = scaler.fit_transform(data_training)

# Connect with keras_model.h5 I've designed
model = load_model('keras_model.h5')

# adding 100 record of data_training to data_testing
past_100_days = data_training.tail(100)
final_df = past_100_days.append(data_testing, ignore_index = True)
input_data = scaler.fit_transform(final_df)

#define x & y test
x_test = []
y_test = []

# Append data from 101 in x_test
# Append data from i to 0 in y_test
for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100: i])
    y_test.append(input_data[i, 0])

x_test, y_test = np.array(x_test) , np.array(y_test)

# Call predict(x_test)
y_predicted = model.predict(x_test) 
scaler = scaler.scale_

scale_factor = 1/scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor

# Create Prediction Price VS Close Price VS Time Chart
st.subheader('Prediction vs Original')
fig2 = plt.figure(figsize=(12,6))
plt.plot(y_test, 'b', label = 'Original Price')
plt.plot(y_predicted, 'r', label = 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)
