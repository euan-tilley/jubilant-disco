import time 
import datetime

e = 1667388815812 / 1000.0

dt = datetime.datetime.utcfromtimestamp(e)
iso_format = dt.isoformat(timespec='milliseconds') + 'Z'

msg = "the is a rds query"

print(f"{iso_format} {msg}")