from celery import shared_task
from .models import Interview
from .emails import send_interview_reminder

@shared_task
def remind_about_interview():
    """ Test for the celery task """

    for interview in Interview.in_range_of_days(15):
        users = interview.interviewees.all()
        vacancy = interview.vacancy
        send_interview_reminder(users, vacancy, interview)
