#To be run via Cron jobs.

"""
Send emails to all subscribers who are registered.
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from emailsubs.models import EmailSubscription, EmailSent
from zobpress.models import Board

boards = Board.objects.all()

for board in boards:
    subscribeds = EmailSubscription.objects.filter(board = board)
    email_sent = EmailSent.objects.get(board = board)
    email_sent.num_times_sent = email_sent.num_times_sent  + 1
    email_sent.save()
    jobs = Job.objects.filter(board = board, created_on__gt = email_sent.updated_on)
    for subscribed in subscribeds:
        if subscribed.send_jobs_email:
            payload = {'jobs':jobs}
            email_txt = render_to_string('emailsubs/job_email.txt', payload)
            send_mail('Job posted at %s'%board.name, email_txt, settings.EMAIL_SENDER, [subscribed.email])
        if subscribed.send_employee_email:
            payload = {'jobs':jobs}
            email_txt = render_to_string('emailsubs/employee_email.txt', payload)
            send_mail('People added at %s'%board.name, email_txt, settings.EMAIL_SENDER, [subscribed.email])
            