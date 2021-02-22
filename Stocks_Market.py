import warnings
warnings.filterwarnings('ignore')  # Hide warnings
from datetime import date
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import matplotlib.pyplot as plt
import os
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
import pickle
from datetime import timedelta

#Importing Libraries done

#title
st.title('Predicting TSLA FUTURE STOCK PRICES')
'---------------------------------------------------------'
#text
st.write("Developed by Benjamin Long")

today = date.today()
# dd/mm/YY
d1 = today.strftime("%Y/%m/%d")

#com = st.sidebar.selectbox("Select a stock",("FB","TSLA"))

st_date= st.sidebar.text_input("Enter Starting date as YYYY/MM/DD", "2020/01/01")

end_date= st.sidebar.text_input("Enter Ending date as YYYY/MM/DD", str(d1))

future_days = st.sidebar.slider('Days to Predict:', min_value=1,max_value=10)

df = web.DataReader("TSLA", 'yahoo', st_date, end_date)  # Collects data

#title
st.title('Stock Market Data')

'The Complete Stock Data as extracted from Yahoo Finance: '
df

'1. The Stock Open Values over time: '
st.line_chart(df["Open"])

'2. The Stock Close Values over time: '
st.line_chart(df["Close"])

df = df.reset_index()


x_future = df.drop(['High','Date','Low','Volume','Adj Close','Open'], 1)[:-future_days]
x_future = x_future.tail(future_days)
x_future = np.array(x_future)

filename_dt = 'dt_stock_model.sav'
loaded_model_dt = pickle.load(open(filename_dt, 'rb'))
result = loaded_model_dt.predict(x_future)


EndDate = date.today()+timedelta(future_days)
StartDate = date.today()+timedelta(days=1)

st.write("Predicted Close value from ",StartDate, "to", EndDate)
st.write(result)

st.title('Visualize Machine learning Model Predicted Data')

df['Prediction'] = df[['Close']].shift(-future_days)
X = np.array(df.drop(['Prediction'], 1))[:-future_days]

valid = df[X.shape[0]:]
valid['Prediction'] = result
fig = plt.figure(figsize=(16,8))
plt.title('Decision Tree Model')
plt.xlabel('Days')
plt.ylabel('Close Price USD ($)')
plt.plot(df[['Close', 'Prediction']])
plt.legend(['Org','Val','Pred'])
st.pyplot(fig)

st.title("Note")
'------------------------------------------------------'
'All Stock data from Yahoo Finance'
'Accurately enter the stock code and date'
'Stock Prices in USD'
