import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout
from tensorflow.keras.layers import LSTM

data=requests.get('https://api.twelvedata.com/time_series?symbol=BTC/INR&interval=5min&outputsize=5000&apikey=%api%key').json()
data_final=pd.DataFrame(data['values'])
print(data_final)
scaler=MinMaxScaler(feature_range=(0,1))
scaled_data=scaler.fit_transform(data_final['close'].values.reshape(-1,1))
timeinterval=24
prediction=12

x_train=[]
y_train=[]

for i in range(timeinterval,len(scaled_data)-prediction):
  x_train.append(scaled_data[i-timeinterval:i,0])
  y_train.append(scaled_data[i+prediction,0])

x_train=np.array(x_train)
y_train=np.array(y_train)
x_train=np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))

model=Sequential()

model.add(LSTM(128,return_sequences=True,input_shape=(x_train.shape[1],1),activation='relu'))
model.add(Dropout(0.4))
model.add(LSTM(64,return_sequences=True,activation='relu'))
model.add(Dropout(0.3))
model.add(LSTM(32,activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='mean_squared_error',optimizer='adam',metrics=['accuracy'])
model.fit(x_train,y_train,epochs=10,batch_size=30)

testapi='https://api.twelvedata.com/time_series?symbol=BTC/INR&interval=5min&outputsize=3000&apikey=%api%key'
testdata=requests.get(testapi).json()
testdatafinal=pd.DataFrame(testdata['values'])

bitcoinprice=pd.to_numeric(testdatafinal['close'],errors='coerce').values
testinputs=testdatafinal['close'].values
testinputs=testinputs.reshape(-1,1)
modelinputs=scaler.fit_transform(testinputs)

x_test=[]
for x in range(timeinterval,len(modelinputs)):
  x_test.append(modelinputs[x-timeinterval:x,0])

x_test=np.array(x_test)
x_test=np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))
prediction_price=model.predict(x_test)
prediction_price=scaler.inverse_transform(prediction_price)

plt.plot(bitcoinprice,label='Bitcoin Prices')
plt.plot(prediction_price,label='Predicted Prices')
plt.title('Predicting Bitcoin Price')
plt.xlabel('5min Interval')
plt.ylabel('Price')
plt.legend()
plt.show()

lastdata=modelinputs[len(modelinputs)+1-timeinterval:len(modelinputs)+1,0]
lastdata=np.array(lastdata)
lastdata=np.reshape(lastdata,(1,lastdata.shape[0],1))
prediction=model.predict(lastdata)
prediction=scaler.inverse_transform(prediction)
print(prediction)
