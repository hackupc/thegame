from datetime import datetime, timedelta

import pytz
from django.conf import settings


def finished():
    now = pytz.utc.localize(datetime.now())
    return now > (getattr(settings, 'ENDING_TIME', None) or (now + timedelta(hours=10)))


def get_substitutions_templates(request):
    return {
        'app_name': settings.APP_NAME,
        'app_description': 'The game is easy! Go and try to solve all challenges!',
        'finished': finished(),
    }
