from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import linebreaks, urlize
from django.conf import settings

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
def get_location(job):
    return ""#TODO

@register.filter
def strip(s):
    return s.strip()

@register.filter
def get_job_board_pages(board):
    return Page.objects.filter(board = board)

from PIL import Image, ImageDraw, ImageFont #@UnresolvedImport
import md5
import os
import sys

FONT_PATH = os.path.join(settings.MEDIA_ROOT, "font/Trebuchet_MS_Bold_Italic.ttf")
FONT_SIZE = 16
FONTCOLOR = "#888"

@register.filter
def mailhide(value):
    import ipdb
    #ipdb.set_trace()
    email_md5 = md5.new(value).hexdigest()
    email_path = os.path.join(settings.MEDIA_ROOT, settings.EMAIL_THUMBNAILS).replace('\\', '/')
    em_file_path = os.path.join(email_path, email_md5 + '.png').replace('\\', '/')
    if not os.path.exists(email_path):
        os.mkdir(email_path)
    if not os.path.exists(em_file_path):
        img = Image.new('RGBA',(1,1))
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        draw = ImageDraw.ImageDraw(img)
        w,h = draw.textsize(value, font)
        img = img.resize((w,h))
        draw = ImageDraw.ImageDraw(img)
        draw.text((0,0),value, font=font, fill=FONTCOLOR)
        img.save(em_file_path)
    
    result = '<img src = "%s%s/%s.png"/>'%(settings.MEDIA_URL, settings.EMAIL_THUMBNAILS, email_md5)
    
    return mark_safe(result)
