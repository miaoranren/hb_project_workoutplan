#!/usr/bin/env python

from datetime import datetime, timedelta

dt = datetime.today()
print(dt.strftime('%Y-%m-%d'))

start_day_of_week_monday = dt - timedelta(days=dt.weekday())
start_day_of_week_tuesday = start_day_of_week_monday + timedelta(days=1)
start_day_of_week_wednesday = start_day_of_week_monday + timedelta(days=2)
start_day_of_week_thursday = start_day_of_week_monday + timedelta(days=3)
start_day_of_week_friday =  start_day_of_week_monday + timedelta(days=4)
start_day_of_week_saturday = start_day_of_week_monday + timedelta(days=5)
end_day_of_week_sunday = start_day_of_week_monday + timedelta(days=6)
start_day_of_week_monday.strftime('%Y-%m-%d')
start_day_of_week_tuesday.strftime('%Y-%m-%d')
start_day_of_week_wednesday.strftime('%Y-%m-%d')
start_day_of_week_thursday.strftime('%Y-%m-%d')
start_day_of_week_friday.strftime('%Y-%m-%d')
start_day_of_week_saturday.strftime('%Y-%m-%d')
end_day_of_week_sunday.strftime('%Y-%m-%d')

