from django.contrib.contenttypes.models import ContentType
from .models import Feedback
from authorization.models import User


class FeedbacksQuery:
    """
    Feedbacks quering class.

    Retrieve list of feedbacks based on the parameters
    """

    def __init__(self, current_user):
        """
        Init query object.

        :param current_user: Instance of user class
        :return: New instance of FeddbacksQuery
        """
        self.current_user = current_user

    def mine(self):
        """
        Feedbacks on user.

        :return: QuerySet of feedbacks for the user
        """

        return Feedback.objects.filter(
            object_id=self.current_user.id,
            content_type=ContentType.objects.get_for_model(User)
        )

    def others(self):
        """
        User's feedbacks on other people.

        :return: QuerySet of feedbacks on other users
        """

        return Feedback.objects.filter(user_id=self.current_user.id)
