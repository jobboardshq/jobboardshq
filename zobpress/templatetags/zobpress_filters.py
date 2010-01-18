from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import linebreaks, urlize
from zobpress.models import Page

register = template.Library()

@register.filter
def prettify(data):
    "Take a Zobdata and return a pretty reprsentation of it."
    if data.data_type == 'BooleanField':
        if data.value:
            return 'Yes'
        else:
            return 'No'
    if data.data_type == 'FileField':
        return mark_safe('<a href="%s">%s</a>' % (data.get_absolute_url(), data.value))
    if data.data_type == 'TextField':
        #return urlize(data.value)
        return linebreaks(urlize(data.value))
    return data.value

@register.filter
def strip(s):
    return s.strip()

@register.filter
def get_job_board_pages(board):
    return Page.objects.filter(job_board = board)
