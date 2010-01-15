#To be run via Cron jobs.

from django.core.management import setup_environ
import settings
setup_environ(settings)

"""
Send emails to all subscribers who are registered.
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from emailsubs.models import EmailSubscription, EmailSent
from zobpress.models import Board, Job


boards = Board.objects.all()

for board in boards:
    subscribeds = EmailSubscription.objects.filter(board = board, is_confirmed = True)
    email_sent = EmailSent.objects.get(board = board)
    jobs = Job.objects.filter(board = board, created_on__gt = email_sent.updated_on)
    email_sent.num_times_sent = email_sent.num_times_sent  + 1
    for subscribed in subscribeds:
        if subscribed.send_jobs_email and jobs:
            payload = {'jobs':jobs, 'board':board}
            email_txt = render_to_string('emailsubs/job_email.txt', payload)
            send_mail('Job posted at %s'%board.name, email_txt, settings.EMAIL_SENDER, [subscribed.email])
            