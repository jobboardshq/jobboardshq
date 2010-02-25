"""
This module populates an arbitrary board with sample data
"""
from django.core.management import setup_environ
import settings
setup_environ(settings)

from zobpress.models import *
board = Board.objects.get(subdomain='board1')

cats = ['Accounting111',
        'Admin-Clerical111',
        'Automotive11',
        'Banking22',
        'Biotech22',
        'Customer Service33',
        'Design22']

jobs = ['Software Engineer',
        'LAMP Stack Specialist',
        'Web Developer / Production Assistant',
        'Digital Education Coordinator',
        'User Experience Specialist',
        'Senior Manager Interactive Development',
        'Software User Interface Designer/Developer',
        'Wanted: Killer graphic designer with mad skillz.',
        'Graphic Design Intern',
        'LAMP Stack Specialist',
        'Web Developer / Production Assistant',
        'Digital Education Coordinator',
        'User Experience Specialist',
        'Senior Manager Interactive Development',
        'Software User Interface Designer/Developer',
        'Wanted: Killer graphic designer with mad skillz.',
        'Graphic Design Intern',
        'LAMP Stack Specialist',
        'Web Developer / Production Assistant',
        'Digital Education Coordinator',
        'User Experience Specialist',
        'Senior Manager Interactive Development',
        'Software User Interface Designer/Developer',
        'Wanted: Killer graphic designer with mad skillz.']

from random import randint

job_types = JobType.objects.filter(board=board)
job_types_len = job_types.count()
assert job_types_len > 0

def get_job_type():
    return job_types[randint(0,job_types_len-1)]

#Create categories
categories = [Category.objects.get_or_create(name=el,board=board) for el in cats]
categories = [el[0] for el in categories]

category_len = len(categories)

def get_a_category():
    return categories[randint(0,category_len-1)]

from django.contrib.webdesign import lorem_ipsum

job_objects = [Job.objects.get_or_create(
    board = board,
    name = el,
    job_type = get_job_type(),
    category = get_a_category(),
    description = lorem_ipsum.paragraphs(3),
    is_active=True,
) for el in jobs]





