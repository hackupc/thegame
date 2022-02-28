import os
from datetime import datetime
import pytz

ATTEMPTS_PER_5_MINUTES = os.environ.get('ATTEMPTS_PER_5_MINUTES', 5)
APP_NAME = 'Advent of HackUPC'
ENDING_TIME = os.environ.get('ENDING_TIME', None)  # Day/Month/Year Hour:Minute from Barcelona Time
if ENDING_TIME is not None:
    ENDING_TIME = pytz.timezone('Europe/Madrid').localize(datetime.strptime(ENDING_TIME, "%d/%m/%Y %H:%M"))\
        .astimezone(pytz.utc)
