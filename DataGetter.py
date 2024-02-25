import requests
import pandas as pd
from datetime import datetime, timedelta



def getdata():
    # Get current date and time
    now = datetime.now()
    now.replace(microsecond=0)

    # Calculate yesterday's date and time
    enddate = (now - timedelta(hours=1)).replace(microsecond=0)

    # Calculate the day before yesterday's date and time
    startdate = (now - timedelta(hours=25)).replace(microsecond=0)

    #date formatting
    startdate.strftime("%Y-%m-%d %H:%M:%S")
    enddate.strftime("%Y-%m-%d %H:%M:%S")

    # print("start",startdate)
    # print("end",enddate)

    #url
    getter=f"https://api.twelvedata.com/time_series?apikey=e76157c75c3a42649e168c5c206e88ca&interval=1h&order=asc&start_date={startdate}&end_date={enddate}&format=JSON&symbol=BTC/INR"

    #getting api response
    response = requests.get(getter).json()

    #formatting metadata
    table=response['values']

    print(pd.DataFrame(table))
    