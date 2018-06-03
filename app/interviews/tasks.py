from celery.task import periodic_task
from celery.task.schedules import crontab
from .models import Interview
from common.services import EmailService
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification, EMAIL

ONE_DAY = 1


@periodic_task(run_every=crontab(minute=0, hour='*'))
def remind_about_interview():
    """Test for the celery task."""

    for interview in Interview.in_range_of_days(ONE_DAY):
        users = interview.interviewees.all()
        for user in users:
            notification = get_notification(user, interview)

            if notification is None:
                vacancy = interview.vacancy
                EmailService.send_interview_reminder(user, vacancy, interview)
                Notification.objects.create(
                    user_id=user.id, object_id=interview.id, type=EMAIL,
                    content_type=get_content_type_for_model(Interview)
                )


def get_notification(user, interview):
    """
    Return existed notification for this particular object.

    :param user: User class instance
    :param interview: Interview class instance
    :return: returns instance of Notification or None
    """

    try:
        return Notification.objects.get(
            user_id=user.id, object_id=interview.id,
            content_type=get_content_type_for_model(Interview)
        )
    except Notification.DoesNotExist:
        return None


def get_content_type_for_model(model):
    """Return ContentType for particular model."""

    return ContentType.objects.get_for_model(model)
