from datetime import timezone, datetime

d = datetime.strptime("May 01 2021 07:00:00 GMT+0000", "%b %d %Y %H:%M:%S %Z+0000")
print(d)