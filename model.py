import os,requests
from datetime import datetime,timedelta
import pandas as pd, numpy as np , matplotlib as plt
from sklearn.preprocessing import MinMaxScaler
from keras.layers import Dense,Dropout,LSTM,Bidirectional
from keras.models import Sequential

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
def getdata():
    # Get current date and time
    now = datetime.now()
    now.replace(microsecond=0)

    # Calculate start and end limits
    enddate = (now - timedelta(days=1)).replace(microsecond=0)
    startdate = (now - timedelta(days=30)).replace(microsecond=0)

    #date formatting
    startdate.strftime("%Y-%m-%d %H:%M:%S")
    enddate.strftime("%Y-%m-%d %H:%M:%S")

    # print("start",startdate)
    # print("end",enddate)

    #url & getting api response
    getter=f"https://api.twelvedata.com/time_series?apikey=e76157c75c3a42649e168c5c206e88ca&interval=1h&order=asc&start_date={startdate}&end_date={enddate}&format=JSON&symbol=BTC/INR"
    response = requests.get(getter).json()

    #formatting metadata
    table=response['values']

    return pd.DataFrame(table)
    
data=getdata()

scaler= MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_tranform(data['close'].values.reshape(-1,1))

