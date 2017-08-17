from . import serializers, User, Company, CompanyMember
from .company_member_serializer import CompanyMemberSerializer
from authorization.serializers import UserSerializer
from django.db.utils import IntegrityError
from rest_framework.authtoken.models import Token

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

import os

class EmployeeSerializer(UserSerializer):
    """ Company employee serializer class """

    emails = serializers.ListField(write_only=True, required=True,
        max_length=10, child=serializers.CharField()
    )
    company_id = serializers.IntegerField(write_only=True, required=True)
    roles = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ('emails', 'company_id', 'roles',)
        read_only_fields = UserSerializer.Meta.fields

    def get_roles(self, obj):
        """ Receiving list of Employee objects """

        company_id = self.context.get('company_id')
        queryset = CompanyMember.objects.filter(user_id=obj.id,
                                                company_id=company_id)
        return CompanyMemberSerializer(queryset, many=True, read_only=True).data

    def create(self, data):
        """
        Creates a new employee if they are do not exist;
        Send invintation emails
        """

        try:
            for email in data['emails']:
                user = self.find_or_create_user(email)
                token, _ = Token.objects.get_or_create(user=user)
                company = Company.objects.get(id=data['company_id'])
                self.send_invite(user, token, company)
            return True
        except IntegrityError:
            return False

    def send_invite(self, user, token, company):
        link_url = '{}/companies/{}/invite'.format(
            os.environ['DEFAULT_CLIENT_HOST'],
            company.id
        )
        msg = render_to_string('company_invite.html', {
                          'company': company,
                          'link_url': link_url,
                          'token': token }
                         )
        send_mail("Company invite mail", msg,
                  "Anymail Sender <from@example.com>", [user.email])


    def find_or_create_user(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(email=email)
        return user
