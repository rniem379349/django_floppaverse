from datetime import datetime

from django.utils import timezone


def get_time_elapsed_humanized(timestamp):
    """
    Return a string saying how much time has elapsed since a given time.
    """
    now = timezone.now()
    if not isinstance(timestamp, datetime):
        return ""
    difference = now - timestamp

    unit_of_time_str = ""
    unit_of_time_num = 0

    if difference.days > 0:
        if difference.days == 1:
            unit_of_time_str = "day"
            unit_of_time_num = 1
        elif 1 < difference.days < 7:
            unit_of_time_str = "days"
            unit_of_time_num = difference.days
        elif 7 <= difference.days < 14:
            unit_of_time_str = "week"
            unit_of_time_num = difference.days // 7
        elif 14 <= difference.days < 30:
            unit_of_time_str = "weeks"
            unit_of_time_num = difference.days // 7
        elif 30 <= difference.days < 60:
            unit_of_time_str = "month"
            unit_of_time_num = difference.days // 30
        elif 60 <= difference.days < 365:
            unit_of_time_str = "months"
            unit_of_time_num = difference.days // 30
        elif 365 <= difference.days < 730:
            unit_of_time_str = "year"
            unit_of_time_num = difference.days // 365
        else:
            unit_of_time_str = "years"
            unit_of_time_num = difference.days // 365
    elif difference.days == 0:
        if difference.seconds < 300:
            return "seconds"
        elif 300 <= difference.seconds < 3600:
            unit_of_time_str = "minutes"
            unit_of_time_num = difference.seconds // 60
        elif 3600 <= difference.seconds < 7200:
            unit_of_time_str = "hour"
            unit_of_time_num = difference.seconds // 3600
        elif 7200 <= difference.seconds < 86400:
            unit_of_time_str = "hours"
            unit_of_time_num = difference.seconds // 3600

    return "%i %s" % (unit_of_time_num, unit_of_time_str)
