from datetime import datetime

import pytz
from django.conf import settings


def print_time_job():
    time_zone = pytz.timezone(settings.TIME_ZONE)
    now = datetime.now(time_zone)
    print(f"Текущее время: {now}")
