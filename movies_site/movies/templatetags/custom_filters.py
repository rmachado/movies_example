from datetime import timedelta
from math import floor
from django import template

register = template.Library()

@register.filter
def duration(total_minutes):
    hours = floor(total_minutes / 60)
    minutes = total_minutes % 60

    if hours >= 1:
        return "{0}h {1}min".format(hours, minutes)
    else:
        return "{0}min".format(minutes)
