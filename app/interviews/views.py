from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import InterviewSerializer
from common.serializers.base_interview_serializer import (
    BaseInterviewSerializer
)
from companies.models import Company
from vacancies.models import Vacancy
from authorization.models import User
from django.db.models import Q
from .models import Interview, InterviewEmployee
from .permissions import InterviewPermission
import ipdb


class InterviewViewSet(viewsets.ModelViewSet):
    """View class for Interviews."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, InterviewPermission, )
    serializer_class = InterviewSerializer

    def get_serializer_class(self):
        """Get serializer class base on action."""

        if self.action == 'list':
            return BaseInterviewSerializer
        else:
            return InterviewSerializer

    def get_queryset(self):
        """Return interviews where current user is participated."""

        current_user = self.request.user
        params = self.kwargs
        company = get_object_or_404(Company, pk=params['company_pk'])
        queryset = Interview.objects.filter(
            Q(candidate=current_user) |
            Q(interviewees__in=[current_user.id]),
            vacancy__company__id=company.id
        )

        if self.action == 'list':
            queryset = queryset.prefetch_related(
                'candidate', 'candidate__avatars'
            )

        return queryset

    def create(self, request, company_pk=None):
        """Create a new interview."""

        get_object_or_404(Company, pk=company_pk)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid() and serializer.save():
            return Response(
                {'interview': serializer.data}, status=status.HTTP_201_CREATED
            )
        else:
            return Response({'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, company_pk=None):
        """Update the interview instance."""

        get_object_or_404(Company, pk=company_pk)
        interview = get_object_or_404(Interview, pk=pk)

        serializer = self.serializer_class(
            interview, data=request.data, partial=True
        )
        if serializer.is_valid() and serializer.save():
            return Response(
                {'interview': serializer.data}, status=status.HTTP_200_OK
            )
        else:
            return Response({'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class InterviewEmployeeView(APIView):
    """View class for InterviewEmployee."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def delete(self, request, interview_id=None, employee_id=None):
        """Delete InterviewEmployee instance."""

        try:
            interview = get_object_or_404(Interview, pk=interview_id)
            employee = get_object_or_404(User, pk=employee_id)
            interview_employee = InterviewEmployee.objects.get(
                employee_id=employee.id, interview_id=interview.id
            )
            interview_employee.delete()
            return Response(
                {'message': 'Succesfully deleted'},
                status=status.HTTP_204_NO_CONTENT
            )
        except InterviewEmployee.DoesNotExist:
            return Response(
                {'detail': 'There is no such user'},
                status=status.HTTP_404_NOT_FOUND
            )
