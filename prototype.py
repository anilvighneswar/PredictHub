import requests
import pandas as pd
from datetime import datetime, timedelta

# Get current date and time
now = datetime.now()
now.replace(microsecond=0)

# Calculate yesterday's date and time
enddate = (now - timedelta(days=1,hours=0,minutes=0,seconds=0)).replace(microsecond=0)

# Calculate the day before yesterday's date and time
startdate = (now - timedelta(days=2)).replace(microsecond=0)

#date formatting
startdate.strftime("%Y-%m-%d %H:%M:%S")
enddate.strftime("%Y-%m-%d %H:%M:%S")

# print("start",startdate)
# print("end",enddate)

#url
getter=f"https://api.twelvedata.com/time_series?apikey=e76157c75c3a42649e168c5c206e88ca&interval=1h&start_date=2024-02-12 19:31:00&end_date=2024-02-13 19:31:00&format=JSON&symbol=BTC/USD&outputsize=10"

#getting api response
response = requests.get(getter).json()

#formatting metadata
table=response['values']

print(pd.DataFrame(table))
    