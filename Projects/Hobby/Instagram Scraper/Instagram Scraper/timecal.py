"2021-01-22T08:27:32.000Z"
from datetime import datetime

post_date = "2021-01-22T08:27:32.000Z"
now = str(datetime.now())

year = int(now[0:4]) - int(post_date[0:4])
month = int(now[5:7]) - int(post_date[5:7])
day = int(now[8:10]) - int(post_date[8:10])

hours = int(now[11:13]) - int(post_date[11:13])
minutes = int(now[14:16]) - int(post_date[14:16])
seconds = int(now[17:19]) - int(post_date[17:19])

if month < 0:
    year -= 1
    month_new = 12 + month
    month = month_new

if day < 0:
    month -= 1
    day_new = 30 + day
    day = day_new

if hours < 0:
    day -= 1
    hours_new = 24 + hours
    hours = hours_new

if minutes < 0:
    hours -= 1
    minutes_new = 60 + minutes
    minutes = minutes_new

if seconds < 0:
    minutes -= 1
    seconds_new = 60 + seconds
    seconds = seconds_new

print(datetime.now())


print(f"years:{year}, moths:{month}, days:{day}")
print(f"hours:{hours}, minutes:{minutes}, seconds:{seconds}")