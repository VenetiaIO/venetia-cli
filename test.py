from datetime import timezone, datetime
import time

date = "May 06 2021 07:00:00 GMT+0000"

d = datetime.strptime(date, "%b %d %Y %H:%M:%S %Z+0000")
# "May 01 2021 07:00:00 GMT+0000"
date = int(datetime.timestamp(d))
time_until_drop = date - int(time.time())

print(date)

print(time_until_drop)