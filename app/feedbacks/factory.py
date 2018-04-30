import factory
from feedbacks.models import Feedback


class FeedbackFactory(factory.django.DjangoModelFactory):
    """ Factory for the feedback model """

    class Meta:
        model = 'feedbacks.Feedback'

    description = factory.Faker('text')
    status = Feedback.ASSIGNED
