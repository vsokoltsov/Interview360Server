from . import serializers, User, Company, CompanyMember, Role
from .company_member_serializer import CompanyMemberSerializer
from authorization.serializers import UserSerializer
from django.db.utils import IntegrityError
from rest_framework.authtoken.models import Token

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

import os
import ipdb

class EmployeeSerializer(UserSerializer):
    """ Company employee serializer class """

    company_id = serializers.IntegerField(write_only=True, required=True)
    emails = serializers.ListField(write_only=True, required=True,
        max_length=10, child=serializers.CharField()
    )
    role_id = serializers.IntegerField(write_only=True, required=True)
    role = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ('emails', 'company_id', 'role', 'role_id')
        read_only_fields = UserSerializer.Meta.fields

    def get_role(self, obj):
        """ Get role for the employee """

        company_id = self.context.get('company_id')
        company_member = CompanyMember.objects.get(user_id=obj.id,
                                                company_id=company_id)
        return CompanyMemberSerializer(company_member, read_only=True).data

    def validate_role_id(self, val):
        """ Set employee role """
        try:
            self.role = Role.objects.get(id=val)
        except Role.DoesNotExist:
            raise serializers.ValidationError('There is no such role')

    def validate_emails(self, value):
        if not value:
            raise serializers.ValidationError({'emails': "Can't be blank"})

        if self.context['user'].email in value:
            raise serializers.ValidationError(
                "You can't add yourself to the company"
            )
        return value

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
                CompanyMember.objects.create(
                    user_id=user.id, company_id=company.id,
                    role_id=self.role.id
                )
                self.send_invite(user, token, company)
            return True
        except IntegrityError as error:
            self.errors['emails'] = 'One of these users already belongs to a company'
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
