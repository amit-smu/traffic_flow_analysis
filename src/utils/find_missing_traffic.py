from datetime import datetime
from datetime import timedelta
import pandas as pd

INTERVAL = 6 # mimnutes
epoch = "2021-08-06-23:12:00"
epoch = datetime.strptime(epoch, "%Y-%m-%d-%H:%M:%S")
delta = timedelta(minutes=INTERVAL)
new_dt = epoch
end = datetime.now()

traffic_data = pd.read_csv()
while new_dt <= end:




