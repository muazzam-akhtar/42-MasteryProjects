import datetime

months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
    ]
past_dt = datetime.datetime(1970, 1, 1)
current_dt = datetime.datetime.now()
delta = (current_dt - past_dt)
print(
    "Seconds since January 1, 1970:",
    "{:,.4f}".format(delta.total_seconds()), "or",
    "{:.2e}".format(delta.total_seconds()), "in scientific notation")
print(months[current_dt.month - 1], current_dt.day, current_dt.year)
